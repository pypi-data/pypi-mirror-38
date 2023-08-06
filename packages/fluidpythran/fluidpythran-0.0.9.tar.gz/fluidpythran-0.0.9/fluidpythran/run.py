"""Command line fluidpythran
============================

Internal API
------------

.. autofunction:: run

.. autofunction:: parse_args

"""

import argparse
from pathlib import Path
from glob import glob

from . import __version__
from .transpiler import make_pythran_files
from .log import logger, set_log_level
from .util import compile_pythran_files, ext_suffix_short, has_to_build

try:
    import pythran
except ImportError:
    pythran = False


doc = """
fluidpythran: easily speedup your Python code with Pythran

"""


def run():
    """Run the fluidpythran commandline

    See :code:`fluidpythran -h`
    """
    args = parse_args()

    if args.version:
        print(__version__)
        return

    if not args.path:
        print("No python files given. Nothing to do! ✨ 🍰 ✨.")
        return

    if args.verbose is None:
        set_log_level("info")
    elif args.verbose > 0:
        set_log_level("debug")
        logger.debug(args)

    path = args.path

    if isinstance(path, list) and len(path) == 1:
        path = path[0]

    if isinstance(path, list):
        paths = path
    else:
        path = Path(path)
        if path.is_file():
            paths = (path,)
        elif path.is_dir():
            paths = path.glob("*.py")
        else:
            paths = glob(str(path))

    make_pythran_files(paths, force=args.force)

    if not pythran or args.no_pythran:
        return

    # find pythran files not already compiled
    pythran_paths = []
    for path in paths:
        path = Path(path)
        pythran_path = path.parent / "__pythran__" / ("_" + path.name)
        ext_path = pythran_path.with_suffix(ext_suffix_short)
        if has_to_build(ext_path, pythran_path):
            pythran_paths.append(pythran_path)

    compile_pythran_files(pythran_paths, args.pythran_flags, parallel=True)


def parse_args():
    """Parse the arguments"""
    parser = argparse.ArgumentParser(
        description=doc, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", help="Path file or directory.", nargs="*")

    parser.add_argument(
        "-f",
        "--force",
        help="write the file even if it is up-to-date",
        action="store_true",
    )

    parser.add_argument(
        "-V", "--version", help="print version and exit", action="store_true"
    )

    parser.add_argument("-v", "--verbose", help="verbose mode", action="count")

    parser.add_argument(
        "-np",
        "--no-pythran",
        help="do not compile the Pythran files with Pythran",
        action="store_true",
    )

    parser.add_argument(
        "-pf",
        "--pythran-flags",
        help=(
            "Flags sent to Pythran. "
            'Default is "-march=native -DUSE_XSIMD". '
            "There has to be atleast one space in the passed string! "
            'Example: fluidpythran toto.py -pf "-march=native "\n'
        ),
        type=str,
        default="",
    )

    return parser.parse_args()
