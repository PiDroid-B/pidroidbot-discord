"""Message is the part for communication between users and the bot."""

# Standard Library
from logging import getLogger

# Third Party
from discord.ext import commands

# Project
from pidroidbot_discord import _


class PluginMessage(commands.Cog):
    """
    All about communication between users and the bot.

    Multiple inheritance - Diamond problem
    Used by .base.PluginBase
    """

    def __init__(self):
        """Construct all the required attributes of the Plugin."""
        self.log = getLogger(f"plugins.{self.__class__.__name__}")
        self.log.info(_("\t{} loaded").format(self.__class__.__name__))
