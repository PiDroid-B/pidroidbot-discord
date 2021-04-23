"""Inspector contains all main's tools for administrators."""

# TODO : plugins
#   a réorganiser en plugins/<nom plugins>/main.py et default_conf
#   revoir fonctionnement core.py

# Standard Library
from logging import getLogger

# Third Party
from discord.ext import commands

# Project
from pidroidbot_discord.launcher import _


class InspectorToDel:
    """
    Dels sqdqsd fdfz fdsf sdf sds.

    Do nothing yet
    """

    def __init__(self, bot):
        """
        Construct all the required attributes of the Plugin.

        :param bot: Bot managed by launcher
        :type bot: commands.Bot
        """
        self.bot = bot
        self.log = getLogger(f"plugins.{__class__.__name__}")
        self.log.info(_("\t\t{} loaded...").format(__class__.__name__))


class Inspector(commands.Cog):
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
        self.log = getLogger(f"plugins.{__class__.__name__}")
        self.log.info(_("\t\t{} loaded...").format(__class__.__name__))


def setup(bot):  # noqa D103
    bot.add_cog(Inspector(bot))
