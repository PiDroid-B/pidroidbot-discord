"""
All const about this project
"""

import os.path
from os import getenv
from pathlib import Path

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

PLUGIN_DIR = os.path.join(ROOT_DIR, "pidroidbot_discord", "plugins")
LANG_DIR = os.path.join(ROOT_DIR, "locales")
CONF_DIR = getenv("PBD__CONFIG_DIR", os.path.join(ROOT_DIR, "settings"))
