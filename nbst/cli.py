"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: nbst.cli
.. moduleauthor:: Stephen Eaton <seaton@strobotics.com.au>
"""
import os
import platform
import sys

import click
from click_help_colors import HelpColorsMultiCommand
from click_help_colors import version_option
from loguru import logger
from rich.console import Console

from . import _version

LOGGING_LEVELS = {
    1: "ERROR",
    2: "WARNING",
    3: "INFO",
    4: "DEBUG",
}  #: a mapping of `verbose` option counts to logging levels


class AppContext:
    """the Application context object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0
        self.console = Console()
        self.netboxservice = None


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(AppContext, ensure=True)


class ComplexCLI(HelpColorsMultiCommand):
    def list_commands(self, ctx):
        commands_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "commands")
        )
        commands = [
            filename[4:-3]
            for filename in os.listdir(commands_folder)
            if filename.endswith(".py") and filename.startswith("cmd_")
        ]

        commands.sort()
        return commands

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"nbst.commands.cmd_{name}", None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(
    cls=ComplexCLI,
    help_headers_color="yellow",  # type: ignore
    help_options_color="green",  # type: ignore
)
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Enable verbose output level (e.g. '-vvvv' for full 'DEBUG' level).",
)
@version_option(
    version=_version.__version__,
    prog_name="nbst",
    version_color="green",
    prog_name_color="yellow",
    message=f" \n \
    %(prog)s %(version)s   \
      Author: Stephen Eaton \n\n\
      Python: {platform.python_version()} \n \
      System: {platform.system()} \n \
      Platform: {platform.platform()}\n",
)
@pass_info
def cli(app_ctx: AppContext, verbose: int):
    """Welcome to NetBox Sync Tool.

    The swiss army knife for all things NetBox
    """
    app_ctx = AppContext

    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "level": LOGGING_LEVELS[verbose]
                    if verbose in LOGGING_LEVELS
                    else "DEBUG",
                }
            ]
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. " f"(LEVEL={LOGGING_LEVELS[verbose]})"
                if verbose in LOGGING_LEVELS
                else "Verbose logging is enabled. (LEVEL=DEBUG)",
                fg="yellow",
            )
        )
    else:
        logger.remove()

    app_ctx.verbose = verbose
