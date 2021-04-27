# Project
from pidroidbot_discord import _

# Local Folder
from .messages import PluginMessage
from .core import PluginCore


class PluginBase(PluginCore, PluginMessage):
    """
    Plugin Inspector.

    Do nothing yet
    """

    pass
