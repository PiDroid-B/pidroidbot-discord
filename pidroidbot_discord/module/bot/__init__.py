"""Package bot extend discord's bot for improve maintainability."""

# Third Party
from discord.ext import commands

# Project
from pidroidbot_discord.module.tools.config import config
from pidroidbot_discord import _
# from pidroidbot_discord.launcher import _

from asyncio import sleep


class MyBot(commands.Bot):
    """
    Class used to add default behaviour on the bot.

    Manage :

    - default prefix from config (command_prefix)

    """

    def __init__(self):
        """"""
        command_prefix = config["main"]["bot"]["prefix"]
        super().__init__(command_prefix=command_prefix)
        print(_("toto"))

    # @bot.event
    # async def on_ready(self):
    #     """Event called when all plugins are loaded and the bot is logged."""
    #     self.log.info(
    #         _("Logged as [{bot_username}] with ID [{bot_userid}]").format(
    #             bot_username=bot.user.name,
    #             bot_userid=bot.user.id,
    #         )
    #     )
    #     await sleep(1)
    #     # servers' inventory where the bot is registered
    #     if config["main"]["debug"]["what_i_see"]:
    #         try:
    #             log.debug(_("Servers' list :"))
    #             for server in bot.guilds:
    #                 log.debug(_("- Server {servername}").format(servername=server.name))
    #                 log.debug(_("\t- Chans"))
    #                 for channel in server.channels:
    #                     log.debug(f"\t\t{channel.id} - {channel.name}")
    #
    #                 log.debug(_("\t- Roles"))
    #                 for role in server.roles:
    #                     log.debug(f"\t\t {role.id} - {role.name}")
    #         except Exception as e:
    #             log.error(e, exc_info=True)
    #
    #     log.info(_("I'm ready !"))
