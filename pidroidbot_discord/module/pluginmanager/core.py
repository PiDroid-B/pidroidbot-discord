# Standard Library
from logging import getLogger

# Third Party
from discord.ext import commands

# Project
from pidroidbot_discord.launcher import _


class Core(commands.Cog):
    """
    Plugin Inspector.

    Do nothing yet
    """

    def __init__(self, bot):
        """
        Construct all the required attributes of the Plugin.

        :param bot: Bot managed by launcher
        :type bot: commands.Bot
        """
        self.bot = bot
        self.log = getLogger(f"plugins.{self.__class__.__name__}")
        self.log.info(_("\t{} loaded").format(self.__class__.__name__))
