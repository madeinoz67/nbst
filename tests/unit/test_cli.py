#!/usr/bin/env python
"""
.. currentmodule:: test_cli
.. moduleauthor:: Stephen Eaton <seaton@strobotics.com.au>

This is the test module for the project's command-line interface (CLI)
module.
"""
# fmt: off
from click.testing import CliRunner
from click.testing import Result

import nbst.cli as cli
from nbst import __version__
# fmt: on


# To learn more about testing Click applications, visit the link below.
# http://click.pocoo.org/5/testing/


def test_version_displays_library_version():
    """
    Arrange/Act: Run the `version` subcommand.
    Assert: The output matches the library version.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["--version"])
    assert (
        __version__ in result.output.strip()
    ), "Version number should match library version."


def test_version_output():
    """
    Arrange/Act: Run the `version`.
    Assert: The output indicates Python Version.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["--version"])
    assert (
        "Python" in result.output.strip()
    ), "Python Version should be indicated in output."


def test_version_displays_expected_name():
    """
    Arrange/Act: Run the `version` subcommand.
    Assert:  The output matches the library name.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["--version"])
    # fmt: off
    assert 'nbst' in result.output.strip(), \
        "Version messages should contain the CLI name."
    # fmt: on


def test_netbox_command():
    """
    Arrange/Act: Run the `netbox` command.
    Assert:  if netbox command is not found in the output.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["netbox"])
    # fmt: off
    assert "Error: No such command 'netbox'" not in result.output.strip(), \
        "'netbox' command is not found."
    # fmt: on
