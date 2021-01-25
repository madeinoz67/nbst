#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from .__init__ import __version__

LOGGING_LEVELS = {
    1: "ERROR",
    2: "WARNING",
    3: "INFO",
    4: "DEBUG",
}  #: a mapping of `verbose` option counts to logging levels


class Info(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


class ComplexCLI(HelpColorsMultiCommand):
    def list_commands(self, ctx):
        commands = []
        commands_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "commands")
        )
        for filename in os.listdir(commands_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                commands.append(filename[4:-3])

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
    help_headers_color="yellow",
    help_options_color="green",
)
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Enable verbose output level (e.g. '-vvvv' for full 'DEBUG' level).",
)
@version_option(
    version=__version__,
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
def cli(info: Info, verbose: int):
    """Welcome to NetBox Sync Tool."""

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

    info.verbose = verbose
