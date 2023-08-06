"""Simple program to manage gbp-docker container lifecycle."""

__version__ = "18.11.2"

import argparse
import logging
import os
import shlex
import shutil
import sys
from pathlib import Path
from subprocess import DEVNULL, PIPE, STDOUT, run
from time import sleep
from typing import List

import controlgraph
import networkx as nx

IMAGE = "opxhub/gbp"
IMAGE_VERSION = "v2.0.4"
if "CNAME" in os.environ:
    CONTAINER_NAME = os.getenv("CNAME")
else:
    CONTAINER_NAME = "{}-dbp-{}".format(os.getenv("USER"), Path.cwd().stem)

DOCKER_INTERACTIVE = "-it" if sys.stdin.isatty() else "-t"
ENV_UID = "-e=UID={}".format(os.getuid())
ENV_GID = "-e=GID={}".format(os.getgid())
ENV_TZ = "-e=TZ={}".format("/".join(Path("/etc/localtime").resolve().parts[-2:]))
ENV_MAINT_NAME = "-e=DEBFULLNAME={}".format(os.getenv("DEBFULLNAME", "Dell EMC"))
ENV_MAINT_MAIL = "-e=DEBEMAIL={}".format(
    os.getenv("DEBEMAIL", "ops-dev@lists.openswitch.net")
)

OPX_DEFAULT_SOURCES = """\
deb     http://deb.openswitch.net/{0} {1} opx opx-non-free
deb-src http://deb.openswitch.net/{0} {1} opx
"""

MAKE_HEAD = """STAMP = .pkg-stamp
.PHONY: all
all:
ALL_REPOS = \\
"""
MAKE_TAIL = """ALL_REPO_STAMPS := $(patsubst %,%/${STAMP},${ALL_REPOS})
TIMESTAMP = $(shell date '+%F %T')

all: ${ALL_REPO_STAMPS}

${ALL_REPO_STAMPS}: REPO = $(notdir ${@D})
${ALL_REPO_STAMPS}: LOG = ${REPO}.log
${ALL_REPO_STAMPS}:
	@echo ${TIMESTAMP} Starting dbp build ${REPO}
	@CNAME="$${USER}-dbp-parallel-${REPO}" dbp build ${REPO} >${LOG} 2>&1
	@: >$@"""

L = logging.getLogger("dbp")
L.addHandler(logging.NullHandler())


### Commands ##########################################################################


def cmd_build(args: argparse.Namespace) -> int:
    rc = docker_pull_images(args.image, args.dist, check_first=True)
    if rc != 0:
        return rc

    rc = 0
    remove = True

    try:
        workspace = get_workspace(Path.cwd())
    except WorkspaceNotFoundError:
        L.error("Workspace not found.")
        return 1

    # generate build order through dfs on builddepends graph
    if not args.targets:
        dirs = [p for p in workspace.iterdir() if p.is_dir()]
        G = controlgraph.graph(controlgraph.parse_all_controlfiles(dirs))

        isolates = list(nx.isolates(G))
        if args.isolates_first:
            G.remove_nodes_from(isolates)
            args.targets = [Path(i) for i in isolates] + [
                Path(n) for n in nx.dfs_postorder_nodes(G)
            ]
        elif args.isolates_last:
            G.remove_nodes_from(isolates)
            args.targets = [Path(n) for n in nx.dfs_postorder_nodes(G)] + [
                Path(i) for i in isolates
            ]
        elif args.no_isolates:
            G.remove_nodes_from(isolates)
            args.targets = [Path(n) for n in nx.dfs_postorder_nodes(G)]
        else:
            args.targets = [Path(n) for n in nx.dfs_postorder_nodes(G)]

    # Get path relative to workspace
    args.targets = [Path(workspace / p) for p in args.targets]

    if not args.targets:
        return rc

    if args.print:
        print(" ".join([p.stem for p in args.targets]))
        return rc

    if docker_container_exists():
        remove = False
    else:
        rc = docker_run(args.image, args.dist, args.extra_sources, dev=False)
        if rc != 0:
            L.error("Could not run container")
            return rc

    if not docker_container_running(args.dist):
        rc = docker_start(args.dist)
        if rc != 0:
            L.error("Could not start stopped container")
            return rc

    sys.stdout.write(
        "--- Building {} repositories: {}\n".format(
            len(args.targets), " ".join([str(t.stem) for t in args.targets])
        )
    )
    for t in args.targets:
        pkg_format = "1.0"

        if Path(t / "debian/source/format").exists():
            pkg_format = Path(t / "debian/source/format").read_text().strip()

        if args.with_debuild:
            pkg_format = "3.0 (git)"
        if args.with_gbp:
            pkg_format = "3.0 (native)"

        if "3.0 (git)" in pkg_format:
            sys.stdout.write("--- cd {}; debuild\n".format(t.stem))
            sys.stdout.flush()
            rc = dexec_debuild(args.dist, t, args.extra_sources, args.debug)
        else:
            sys.stdout.write("--- cd {}; gbp buildpackage\n".format(t.stem))
            sys.stdout.flush()
            rc = dexec_buildpackage(
                args.dist, t, args.extra_sources, args.gbp, args.debug
            )

        if rc != 0:
            L.error("Could not build package {}".format(t.stem))
            break

    if remove:
        docker_remove_container()

    return rc


def cmd_makefile(args: argparse.Namespace) -> int:
    dirs = [p for p in Path.cwd().iterdir() if p.is_dir()]
    g = controlgraph.graph(controlgraph.parse_all_controlfiles(dirs))
    print(makefile(g))
    return 0


def cmd_pull(args: argparse.Namespace) -> int:
    return docker_pull_images(args.image, args.dist)


def cmd_rm(args: argparse.Namespace) -> int:
    docker_remove_container()
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    rc = docker_pull_images(args.image, args.dist, check_first=True)
    if rc != 0:
        return rc

    return docker_run(args.image, args.dist, args.extra_sources, dev=True)


def cmd_shell(args: argparse.Namespace) -> int:
    rc = docker_pull_images(args.image, args.dist, check_first=True)
    if rc != 0:
        return rc

    remove = True

    if docker_container_exists():
        remove = False
    else:
        rc = docker_run(args.image, args.dist, args.extra_sources, dev=True)
        if rc != 0:
            L.error("Could not run container")
            return rc

    if not docker_container_running(args.dist):
        rc = docker_start(args.dist)
        if rc != 0:
            L.error("Could not start stopped container")
            return rc

    cmd = [
        "docker",
        "exec",
        DOCKER_INTERACTIVE,
        "--user=build",
        deb_build_options_string(args.debug, 0),
        ENV_UID,
        ENV_GID,
        ENV_TZ,
        ENV_MAINT_NAME,
        ENV_MAINT_MAIL,
        "-e=EXTRA_SOURCES={}".format(args.extra_sources),
        CONTAINER_NAME,
        "bash",
        "-l",
    ]

    if args.command:
        cmd.extend(["-c", args.command])

    rc = irun(cmd, quiet=False)

    if remove:
        docker_remove_container()

    return rc


### Docker functions ##################################################################


def dexec_buildpackage(
    dist: str, target: Path, sources: str, gbp_options: str, debug=False
) -> int:
    """Runs gbp buildpackage

    Container must already be started.
    """
    if not target.exists():
        L.error("Build target `{}` does not exist".format(target))
        return 1

    cmd = [
        "docker",
        "exec",
        DOCKER_INTERACTIVE,
        "--user=build",
        "--workdir=/mnt/{}".format(target.stem),
        deb_build_options_string(debug, 0),
        ENV_UID,
        ENV_GID,
        ENV_TZ,
        ENV_MAINT_NAME,
        ENV_MAINT_MAIL,
        "-e=EXTRA_SOURCES={}".format(sources),
        CONTAINER_NAME,
        "gbp",
        "buildpackage",
    ]
    cmd.extend(shlex.split(gbp_options))

    return irun(cmd)


def dexec_debuild(dist: str, target: Path, sources: str, debug=False) -> int:
    """Runs debuild

    Container must already be started.
    """
    if not target.exists():
        L.error("Build target `{}` does not exist".format(target))
        return 1

    cmd = [
        "docker",
        "exec",
        DOCKER_INTERACTIVE,
        "--user=build",
        "--workdir=/mnt/{}".format(target.stem),
        deb_build_options_string(debug, 0),
        ENV_UID,
        ENV_GID,
        ENV_TZ,
        ENV_MAINT_NAME,
        ENV_MAINT_MAIL,
        "-e=EXTRA_SOURCES={}".format(sources),
        CONTAINER_NAME,
        "debuild",
    ]

    return irun(cmd)


def docker_container_exists() -> bool:
    """Returns true if our dbp container can be inspected"""
    return irun(["docker", "inspect", CONTAINER_NAME], quiet=True) == 0


def docker_container_running(dist: str) -> bool:
    """Returns true if our dbp container is running"""
    proc = run(
        ["docker", "inspect", CONTAINER_NAME, "--format={{.State.Running}}"],
        stdout=PIPE,
        stderr=DEVNULL,
    )
    return proc.returncode == 0 and "true" in str(proc.stdout)


def docker_image_name(image: str, dist: str, dev: bool) -> str:
    """Returns the Docker image to use, allowing for custom images."""
    if ":" in image:
        return image

    if dev:
        template = "{}:{}-{}-dev"
    else:
        template = "{}:{}-{}"

    return template.format(image, IMAGE_VERSION, dist)


def docker_pull_images(image: str, dist: str, check_first=False) -> int:
    """Runs docker pull for both build and development images and returns the return code"""
    if ":" in image:
        # manually specified image tag, assume no pull needed
        return 0

    if check_first:
        tag = docker_image_name(image, dist, dev=True)[len(image) + 1 :]
        proc = run(["docker", "images"], stdout=PIPE, stderr=STDOUT)
        if image in proc.stdout.decode("utf-8") and tag in proc.stdout.decode("utf-8"):
            return 0

    print("Pulling Docker image {}".format(image))

    cmd = ["docker", "pull", docker_image_name(image, dist, False)]
    rc = irun(cmd)
    if rc != 0:
        return rc

    cmd = ["docker", "pull", docker_image_name(image, dist, True)]
    return irun(cmd)


def docker_remove_container() -> int:
    """Runs docker rm -f for the dbp container"""
    if docker_container_exists():
        cmd = ["docker", "rm", "-f", CONTAINER_NAME]
        return irun(cmd, quiet=True)

    L.info("Container does not exist.")
    return 1


def docker_run(image: str, dist: str, sources: str, dev=True) -> int:
    if docker_container_exists():
        L.info("Container already exists")
        return 0

    try:
        workspace = get_workspace(Path.cwd())
    except WorkspaceNotFoundError:
        L.error("Workspace not found.")
        return 1

    cmd = [
        "docker",
        "run",
        "-d",
        DOCKER_INTERACTIVE,
        "--name={}".format(CONTAINER_NAME),
        "--hostname={}".format(dist),
        "-v={}:/mnt".format(workspace),
    ]

    gitconfig = Path(Path.home() / ".gitconfig")
    if gitconfig.exists():
        cmd.append("-v={}:/etc/skel/.gitconfig:ro".format(gitconfig))

    cmd.extend(
        [
            ENV_UID,
            ENV_GID,
            ENV_TZ,
            ENV_MAINT_NAME,
            ENV_MAINT_MAIL,
            "-e=EXTRA_SOURCES={}".format(sources),
            docker_image_name(image, dist, dev),
            "bash",
            "-l",
        ]
    )

    rc = irun(cmd, quiet=True)
    # wait for user to be created
    sleep(1)
    return rc


def docker_start(dist: str) -> int:
    """Runs docker start and returns the return code"""
    cmd = ["docker", "start", CONTAINER_NAME]
    return irun(cmd, quiet=True)


### Utilities #########################################################################


def irun(cmd: List[str], quiet=False) -> int:
    """irun runs an interactive command.

    irun returns -1 when no command is specified.
    """
    if len(cmd) == 0:
        return -1

    L.debug("Running {}".format(" ".join(cmd)))
    if quiet:
        proc = run(cmd, stdin=sys.stdin, stdout=DEVNULL, stderr=DEVNULL)
    else:
        proc = run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    return proc.returncode


def deb_build_options_string(debug: bool, parallel=0) -> str:
    opts = []

    if debug:
        opts.extend(["nostrip", "noopt", "debug"])

    if parallel > 0:
        opts.append("parallel={}".format(parallel))

    return "-e=DEB_BUILD_OPTIONS={}".format(" ".join(opts))


def get_workspace(path: Path) -> Path:
    """Check if the current directory is a workspace and return it.

    If not, check if the parent directory is a workspace and return it.
    If not, return the originally supplied path.
    A "Debian repo" is a directory with a ./debian/control file that you own.
    Returns a Path or raises a WorkspaceNotFoundError.
    """
    for p in path.iterdir():
        if p.is_dir():
            try:
                if Path(p / "debian/control").exists():
                    owner = Path(p / "debian/control").owner()
                    if owner == os.getenv("USER", ""):
                        return path
            except PermissionError:
                continue

    if path == Path(path.anchor):
        raise WorkspaceNotFoundError(
            "No workspace found at {} or any directories above it.".format(path)
        )

    for p in path.parent.iterdir():
        if p.is_dir():
            try:
                if Path(p / "debian/control").exists():
                    owner = Path(p / "debian/control").owner()
                    if owner == os.getenv("USER", ""):
                        return path.parent
            except PermissionError:
                continue

    return path


def makefile(g: nx.DiGraph) -> str:
    bob = ""  # the builder
    dep_lines = []  # makefile dependency lines to print

    bob += MAKE_HEAD
    nodes = sorted([n for n in nx.dfs_postorder_nodes(g)])
    for n in nodes:
        if n == nodes[len(nodes) - 1]:
            bob += "\t{n}\n".format(n=n)
        else:
            bob += "\t{n} \\\n".format(n=n)
        for dep in g.successors(n):
            temp = ""
            temp += str(n)
            temp += "/${STAMP}: "
            temp += str(dep)
            temp += "/${STAMP}\n"
            dep_lines.append(temp)
    for line in dep_lines:
        bob += line
    bob += MAKE_TAIL

    return bob


class WorkspaceNotFoundError(FileNotFoundError):
    pass


### Main ##############################################################################


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)

    # general arguments
    parser.add_argument(
        "--version", "-V", action="store_true", help="print program version"
    )
    parser.add_argument(
        "--verbose", "-v", help="-v for info, -vv for debug", action="count", default=0
    )
    parser.add_argument(
        "--debug", help="Set nostrip, noopt, debug", action="store_true"
    )
    parser.add_argument(
        "--dist", "-d", help="Debian distribution", default=os.getenv("DIST", "stretch")
    )
    parser.add_argument(
        "--release", "-r", help="OPX release (default: unstable)", default="unstable"
    )
    parser.add_argument(
        "--extra-sources",
        "-e",
        help="Apt-style sources",
        default=os.getenv("EXTRA_SOURCES", ""),
    )
    parser.add_argument(
        "--no-extra-sources", action="store_true", help="ignore any custom apt sources"
    )
    parser.add_argument("--image", "-i", help="Docker image to use", default=IMAGE)

    sps = parser.add_subparsers(help="commands")

    # build subcommand
    build_parser = sps.add_parser("build", help="run git-buildpackage or debuild")
    build_parser.add_argument(
        "--gbp", "-g", default="", help="additional git-buildpackage options to pass"
    )
    build_parser.add_argument(
        "--print", "-p", action="store_true", help="print build order and exit"
    )
    build_parser.add_argument(
        "targets", nargs="*", type=Path, help="directories to build"
    )
    build_isolates = build_parser.add_mutually_exclusive_group()
    build_isolates.add_argument(
        "--isolates-first", action="store_true", help="build free-standing repos first"
    )
    build_isolates.add_argument(
        "--isolates-last", action="store_true", help="build free-standing repos last"
    )
    build_isolates.add_argument(
        "--no-isolates", action="store_true", help="do not build free-standing repos"
    )
    build_command = build_parser.add_mutually_exclusive_group()
    build_command.add_argument(
        "--with-debuild", action="store_true", help="force building with debuild"
    )
    build_command.add_argument(
        "--with-gbp", action="store_true", help="force building with gbp"
    )
    build_parser.set_defaults(func=cmd_build)

    # makefile subcommand
    makefile_parser = sps.add_parser("makefile", help="create Makefile")
    makefile_parser.set_defaults(func=cmd_makefile)

    # pull subcommand
    pull_parser = sps.add_parser("pull", help="pull latest images")
    pull_parser.set_defaults(func=cmd_pull)

    # rm subcommand
    rm_parser = sps.add_parser("rm", help="remove workspace container")
    rm_parser.set_defaults(func=cmd_rm)

    # run subcommand
    run_parser = sps.add_parser("run", help="run development container in background")
    run_parser.set_defaults(func=cmd_run)

    # shell subcommand
    shell_parser = sps.add_parser("shell", help="launch development environment")
    shell_parser.add_argument("--command", "-c", help="command to run noninteractively")
    shell_parser.set_defaults(func=cmd_shell)

    args = parser.parse_args()

    if args.version:
        print("dbp {}".format(__version__))
        return 0

    # set up logging
    logging.basicConfig(
        format="[%(levelname)s] %(message)s", level=10 * (3 - min(args.verbose, 2))
    )

    # check for prereqs
    if shutil.which("docker") is None:
        L.error("Docker not found in PATH. Please install docker.")
        sys.exit(1)

    # read sources from ./extra_sources.list and ~/.extra_sources.list
    if args.extra_sources == "":
        extra_sources = [
            Path("extra_sources.list"),
            Path.home() / ".extra_sources.list",
        ]
        for s in extra_sources:
            if s.exists():
                args.extra_sources = s.read_text()
                break

    if args.extra_sources == "":
        args.extra_sources = OPX_DEFAULT_SOURCES.format(args.dist, args.release)

    if args.no_extra_sources:
        args.extra_sources = ""

    if args.extra_sources != "":
        L.info("Loaded extra sources:\n{}".format(args.extra_sources))

    # print help if no subcommand specified
    if getattr(args, "func", None) is None:
        parser.print_help()
        return 0

    # run subcommand
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
