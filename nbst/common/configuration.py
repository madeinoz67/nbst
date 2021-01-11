#  Copyright (c) 2021 Stephen Eaton. All rights reserved.
#
#  nbst.py
#
#  This work is licensed under the terms of the MIT license.
#  For a copy, see file LICENSE.txt included in this
#  repository or visit: <https://opensource.org/licenses/MIT>.
import os

import yaml
from loguru import logger as log

from nbst.common.misc import do_error_exit


def get_config_file(config_file):
    """
    get absolute path to provided config file string

    Parameters
    ----------
    config_file: str
        config file path

    Returns
    -------
    str: absolute path to config file
    """

    if config_file is None or config_file == "":
        do_error_exit("ERROR: Config file not defined.")

    base_dir = os.sep.join(__file__.split(os.sep)[0:-3])
    if config_file[0] != os.sep:
        config_file = f"{base_dir}{os.sep}{config_file}"

    return os.path.realpath(config_file)


def open_config_file(config_file):
    """
    Open a yaml config file and return handler. Bail out of opening or parsing fails

    Parameters
    ----------
    config_file: str
        absolute path of config file to open

    Returns
    -------
    ConfigParser: handler with supplied config file
    """

    if config_file is None or config_file == "":
        do_error_exit("ERROR: Config file not defined.")

    # noinspection PyBroadException
    try:
        with open(config_file) as file:
            config = yaml.safe_load(file)
    # noinspection PyBroadException
    except Exception:
        do_error_exit(f"ERROR: Unable to open file '{config_file}'")

    return config


def get_config(config_handler=None, section=None, valid_settings=None):
    """
    read config items from a defined section

    Parameters
    ----------
    config: list
        a full config to read config data from
    section: str
        name of the section to read
    valid_settings: dict
        a dictionary with valid config items to read from this section.
        key: is the config item name
        value: default value if config option is undefined

    Returns
    -------
    dict:   parsed config items from defined $section

    """

    def get_config_option(config, this_section, item, default=None):

        if isinstance(default, bool):
            value = config_handler.getboolean(this_section, item, fallback=default)
        elif isinstance(default, int):
            value = config_handler.getint(this_section, item, fallback=default)
        else:
            value = config_handler.get(this_section, item, fallback=default)

        if value == "":
            value = None

        config_dict[item] = value

        # take care of logging sensitive data
        for sensitive_item in ["token", "pass"]:

            if sensitive_item.lower() in item.lower():
                value = value[0:3] + "***"

        log.debug(f"Config: {this_section}.{item} = {value}")

    config_dict = {}

    if valid_settings is None:
        log.error("No valid settings passed to config parser!")

    # read specified section section
    if section is not None:
        if section not in config_handler.sections():
            log.error(f"Section '{section}' not found in config_file")
        else:
            for config_item, default_value in valid_settings.items():
                get_config_option(section, config_item, default=default_value)

    return config_dict


# EOF
