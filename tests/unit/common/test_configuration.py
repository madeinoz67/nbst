import os

import pytest
import yaml

from nbst.common.configuration import get_config_file
from nbst.common.configuration import open_config_file


@pytest.fixture
def config_file():
    return "./tests/test_files/config1.yml"


def test_valid_get_config_file_path(config_file):

    config_path = get_config_file(config_file)

    assert config_path == os.path.realpath(config_file)


def test_empty_get_config_file_path(capsys):

    with pytest.raises(SystemExit):
        get_config_file("")

    out, err = capsys.readouterr()

    assert out == ""
    assert err == "ERROR: Config file not defined.\n"


def test_valid_open_config_file(config_file):
    config_path = get_config_file(config_file)
    config = open_config_file(config_path)

    with open(config_file) as file:
        expected = yaml.safe_load(file)

    assert len(config) == len(expected)
    assert config == expected
    assert isinstance(config, list)


def test_invalid_open_config_file(capsys):

    with pytest.raises(SystemExit):
        open_config_file("not_a_real_file")

    out, err = capsys.readouterr()

    assert out == ""
    assert err.startswith("ERROR: Unable to open file")


def test_empty_open_config_file(capsys):

    with pytest.raises(SystemExit):
        open_config_file("")

    out, err = capsys.readouterr()

    assert out == ""
    assert err.startswith("ERROR: Config file not defined.")


# def test_get_config_option(config_file):
#     config_path = get_config_file(config_file)
#     open_config_file(config_path)


# option = get_config_option("common", )
