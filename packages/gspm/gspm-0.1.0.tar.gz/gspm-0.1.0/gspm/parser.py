
import argparse
import gspm

from gspm.commands.new import New
from gspm.commands.install import Install
from gspm.commands.edit import Edit

def _create_options(parser):

    parser.add_argument(
        "-f",
        "--force",
        dest="force",
        action="store_true",
        help="force a command to execute with warnings",
        default=False)

    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        help="use a different configuration file",
        default="project.yml")

    parser.add_argument(
        "-V",
        "--verbose",
        dest="verbose",
        help="show more information on console when running",
        default=0)

    parser.add_argument(
        "--version",
        action="version",
        version="",
        help="show version"
    )
    parser.add_argument(
        "--ignore-project",
        default=False,
        help=argparse.SUPPRESS
    )


def _create_commands(subparser):

    new = New()
    new.add_parser(subparser)

    install = Install()
    install.add_parser(subparser)

    edit = Edit()
    edit.add_parser(subparser)


def create_parser():

    parser = argparse.ArgumentParser(prog='gspm', description=gspm.__desc__)
    subparser = parser.add_subparsers(dest='command')
    subparser.required = True

    _create_options(parser)
    _create_commands(subparser)

    return parser
