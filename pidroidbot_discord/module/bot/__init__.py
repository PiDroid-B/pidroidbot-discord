"""Package bot extend discord's bot for improve maintainability."""

# Standard Library
from asyncio import sleep
from logging import getLogger

# Third Party
from discord.ext import commands

# Project
from pidroidbot_discord.module.tools.config import config


class MyBot(commands.Bot):
    """
    Class used to add default behaviour on the bot.

    Manage :

    - default prefix from config (command_prefix)

    """

    def __init__(self, _, __):
        """"""
        command_prefix = config["main"]["bot"]["prefix"]
        # workaround : avoid circular import on global var
        self._ = _
        self.__ = __
        self.log = getLogger("main.Bot")
        super().__init__(command_prefix=command_prefix)

    async def on_ready(self):
        """Event called when all plugins are loaded and the bot is logged."""
        self.log.info(
            self._("Logged as [{bot_username}] with ID [{bot_userid}]").format(
                bot_username=self.user.name,
                bot_userid=self.user.id,
            )
        )
        await sleep(1)
        # servers' inventory where the bot is registered
        if config["main"]["debug"]["what_i_see"]:
            try:
                self.log.debug(self._("Servers' list :"))
                for server in self.guilds:
                    self.log.debug(
                        self._("- Server {servername}").format(servername=server.name)
                    )
                    self.log.debug(self._("\t- Chans"))
                    for channel in server.channels:
                        self.log.debug(f"\t\t{channel.id} - {channel.name}")

                    self.log.debug(self._("\t- Roles"))
                    for role in server.roles:
                        self.log.debug(f"\t\t {role.id} - {role.name}")
            except Exception as e:
                self.log.error(e, exc_info=True)

        self.log.info(self._("I'm ready !"))
