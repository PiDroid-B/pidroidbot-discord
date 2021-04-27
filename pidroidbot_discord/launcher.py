"""
Launcher of the bot.

Manage :

- logging system (log)
- main setting (main.default.yml overrided by main.local.yml if exist)
- pluggins and bot initialization

"""
# Standard Library
import asyncio
import logging.config
import os
from getpass import getuser as getusername

# Third Party
from discord.errors import LoginFailure
from discord.ext import commands

# Project
from pidroidbot_discord import __version__
from pidroidbot_discord.const import CONF_DIR, PLUGIN_DIR
from pidroidbot_discord.default_conf import DEFAULT_CONFIG
from pidroidbot_discord.module.bot import MyBot
from pidroidbot_discord.module.tools.config import config, load_config
from pidroidbot_discord.module.tools.language import load_language
from pidroidbot_discord.module.tools.str_utils import wrap


load_config("main", DEFAULT_CONFIG)
_, __ = load_language(config["main"]["lang"])

logging.config.dictConfig(config["main"]["log"])

log = logging.getLogger("main")
log.info("*" * 80)
log.info(
    " START pidroidbot-discord v{version} [{lang}/{user}] ".format(
        version=__version__,
        lang=config["main"]["lang"],
        user=getusername(),
    ).center(80, "*")
)
log.info("*" * 80)

bot = MyBot(_, __)

# @bot.event
# async def on_ready():
#     """Event called when all plugins are loaded and the bot is logged."""
#     log.info(
#         _("Logged as [{bot_username}] with ID [{bot_userid}]").format(
#             bot_username=bot.user.name,
#             bot_userid=bot.user.id,
#         )
#     )
#     await asyncio.sleep(1)
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


def load_extension():
    """
    Load all extensions in according with the defined list of plugins.

    The list of plugins to load is defined in conf file "main".
    """
    for extension in [
        f.lower() for f in os.listdir(PLUGIN_DIR) if not f.startswith("_")
    ]:
        try:
            if extension in [p.lower() for p in config["main"]["plugins"]]:
                bot.load_extension(f"plugin.{extension}")

        except commands.ExtensionError:
            log.error(
                f'Failed to load extension "{extension}". \n',
                exc_info=True,
            )


def main():
    """Launch the bot."""
    log.info(_("Initialization"))
    try:
        for info in wrap(
            _("Load extensions : {}").format(
                " ".join(config["main"]["plugins"]),
            ),
            width=80,
        ):
            log.info(info)

        load_extension()

        bot.run(config["main"]["bot"]["token"])
    except FileNotFoundError:
        log.error(
            _(
                "No plugin found in plugin' directory...\n\t"
                "Please check your installation"
            )
        )
        exit(1)
    except LoginFailure:
        log.error(
            _(
                "Token is wrong or missing in configuration's file"
                "\n\tPlease check the value for the key [bot][token]"
                "\n\tin {file}"
            ).format(file=f"{os.path.join(CONF_DIR,'main.local.yml')}")
        )
        exit(1)
    finally:
        pass
        # bot.db.close()
    log.info(_("Good bye !!!"))
