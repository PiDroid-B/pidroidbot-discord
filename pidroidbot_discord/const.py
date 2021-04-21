"""All global const about this project."""

# Standard Library
import os.path
from os import getenv
from pathlib import Path


ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

PLUGIN_DIR = os.path.join(ROOT_DIR, "pidroidbot_discord", "plugin")
LANG_DIR = os.path.join(ROOT_DIR, "locales")
CONF_DIR = getenv("PBD__CONFIG_DIR", os.path.join(ROOT_DIR, "setting"))
LOG_DIR = getenv("PBD__LOG_DIR", os.path.join(ROOT_DIR, "log"))

LOG_FILE = os.path.join(LOG_DIR, "pidroidbot_discord.log")
