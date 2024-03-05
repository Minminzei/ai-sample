#!/usr/bin/env python3
import gettext
import locale
import os
import sys

# Translations don't work by default in Windows, so hack in environment variable
if sys.platform.startswith("win"):
    os.environ["LANG"], _ = locale.getdefaultlocale()

from lib.cli import args as cli_args  # pylint:disable=wrong-import-position
from lib.config import generate_configs  # pylint:disable=wrong-import-position

# LOCALES
_LANG = gettext.translation("faceswap", localedir="locales", fallback=True)
_ = _LANG.gettext

if sys.version_info < (3, 10):
    raise ValueError("This program requires at least python 3.10")

_PARSER = cli_args.FullHelpArgumentParser()


def _bad_args(*args) -> None:  # pylint:disable=unused-argument
    print(cli_args)
    _PARSER.print_help()
    sys.exit(0)

def _main() -> None:
    generate_configs()

    subparser = _PARSER.add_subparsers()
    cli_args.ExtractArgs(subparser, "extract", _("Extract the faces from pictures or a video"))
    cli_args.TrainArgs(subparser, "train", _("Train a model for the two faces A and B"))
    cli_args.ConvertArgs(subparser,
                         "convert",
                         _("Convert source pictures or video to a new one with the face swapped"))
    cli_args.GuiArgs(subparser, "gui", _("Launch the Faceswap Graphical User Interface"))
    _PARSER.set_defaults(func=_bad_args)
    arguments = _PARSER.parse_args()
    arguments.func(arguments)


if __name__ == "__main__":
    _main()
