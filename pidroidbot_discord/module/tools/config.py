"""
Manage all configuration's features.

global var config{} contains all setting ordered by key=(pluggin name|main)
filled by function load_config(conf_name, yaml_default_conf)
"""
# Standard Library
import logging
import logging.config
import os
from pathlib import Path
from sys import exit as sysexit

# Third Party
import yaml

# Project
from pidroidbot_discord.const import CONF_DIR


config = {}

# TODO séparer en 2 fonctions (réécrire tous les default_conf + cherger les local_conf)


def load_config(conf_name, yaml_default_conf):
    """
    Load config from files in configuration's directory.

    load configuration from a conf_name and add it to the dict config
    for the same conf_name, <conf_name>.local.yml override <conf_name>.default.yml

    <conf_name>.default.yml will be created if missing (exit(1))
    use env variable PBD__CONFIG_DIR for specific conf path

    :param conf_name: Name of the config (part of file name without extension)
    :type conf_name: string
    :param yaml_default_conf: Content of the config in yaml
    :type yaml_default_conf: string
    """
    # load default conf or create it and exit(1)
    config_content = {}

    config_file_default = os.path.join(CONF_DIR, f"{conf_name}.default.yml")
    config_file_local = os.path.join(CONF_DIR, f"{conf_name}.local.yml")
    try:
        config_content = yaml.safe_load(Path(config_file_default).read_text())
    except IOError:
        with open(config_file_default, "w") as f:
            f.write(yaml_default_conf)
            f.close()
        logging.error(
            f"Didn't find default conf file, autoregenerated into {config_file_default}"
        )
        sysexit(1)

    # if "main" then we load default log conf as the first choice
    # will help for next log in this unit
    if conf_name == "main":
        logging.config.dictConfig(config_content["log"])
    # use log setting of "main"
    log = logging.getLogger("main.config")

    try:
        config_content_local = yaml.safe_load(Path(config_file_local).read_text())
        config_content.update(config_content_local)
        logging.config.dictConfig(config_content["log"])

    #  yaml.scanner.ScannerError
    except yaml.YAMLError as e:
        logging.error(f"YAML syntax error in {config_file_local}\n{e}")
        sysexit(1)
    except FileNotFoundError:
        log.warning(
            f"No {config_file_local} found - default configuration is not overrided"
        )

    config[conf_name] = config_content
