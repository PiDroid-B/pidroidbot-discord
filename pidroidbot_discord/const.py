import os.path
from os import getenv
from pathlib import Path

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

PLUGIN_DIR = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))), "plugins")
LANG_DIR = os.path.join(ROOT_DIR, "locale")
CONF_DIR = getenv("PBD__CONFIG_DIR", os.path.join(ROOT_DIR, "settings"))
