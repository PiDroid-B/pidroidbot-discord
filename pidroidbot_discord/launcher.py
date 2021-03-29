import asyncio
import logging.config
import os

from default_conf import DEFAULT_CONFIG
from discord.errors import LoginFailure
from discord.ext import commands
from pidroidbot_discord import __version__
from pidroidbot_discord.const import CONF_DIR, PLUGIN_DIR
from pidroidbot_discord.module.config import config, load_config
from pidroidbot_discord.module.language import load_language

load_config("main", DEFAULT_CONFIG)
_, __ = load_language(config["main"]["lang"])


logging.config.dictConfig(config["main"]["log"])

log = logging.getLogger("main")
log.info("*" * 80)
log.info(
    " START pidroidbot-discord v{version} [{lang}] ".format(
        version=__version__, lang=config["main"]["lang"]
    ).center(80, "*")
)
log.info("*" * 80)


bot = commands.Bot(command_prefix=config["main"]["bot"]["prefix"])


@bot.event
async def on_ready():
    log.info(
        _("Logged as [{bot_username}] with ID [{bot_userid}]").format(
            bot_username=bot.user.name, bot_userid=bot.user.id
        )
    )
    await asyncio.sleep(1)
    # servers' inventory where the bot is registered
    if config["main"]["debug"]["what_i_see"]:
        try:
            log.debug(_("Servers' list :"))
            for server in bot.guilds:
                log.debug(_("- Server {servername}").format(servername=server.name))
                log.debug(_("\t- Chans"))
                for channel in server.channels:
                    log.debug(f"\t\t{channel.id} - {channel.name}")

                log.debug(_("\t- Roles"))
                for role in server.roles:
                    log.debug(f"\t\t {role.id} - {role.name}")
        except Exception as e:
            log.error(e, exc_info=True)

    log.info(_("I'm ready !"))


def main():

    log.info(_("Initialization"))
    config["main"]["cogs"]["list_ignore"] = ["core"]
    try:
        log.info(_("Load extensions..."))
        log.info(PLUGIN_DIR)
        for extension in [
            f
            for f in os.listdir(PLUGIN_DIR)
            if os.path.isdir(os.path.join(PLUGIN_DIR, f)) and not f.startswith("_")
        ]:
            try:
                if extension not in config["main"]["cogs"]["list_ignore"]:
                    log.info("\t" + extension)
                    bot.load_extension(f"plugins.{extension}")

            except commands.ExtensionError as e:
                log.error(f'Failed to load extension "{extension}". \n', exc_info=True)

        bot.run(config["main"]["bot"]["token"])
    except FileNotFoundError as e:
        log.error(
            _(
                "No plugin found in plugins' directory...\n\tPlease check your installation"
            )
        )
        exit(1)
    except LoginFailure as e:
        log.error(
            _(
                "Token is wrong or missing in configuration's file"
                "\n\tPlease check the value for the key [bot][token]"
                "\n\tin {file}"
            ).format(file=f"{os.path.join(CONF_DIR,'main.local')}")
        )
        exit(1)
    finally:
        pass
        # bot.db.close()
