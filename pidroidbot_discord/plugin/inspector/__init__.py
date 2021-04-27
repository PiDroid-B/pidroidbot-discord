"""Inspector contains all main's tools for administrators."""


# Standard Library
import time

# Third Party
from discord.ext import commands

# Project
from pidroidbot_discord.module.plugin import PluginBase


class Inspector(PluginBase):
    """
    Plugin Inspector.

    Do nothing yet
    """

    @commands.command(brief="Vérifie la latence", pass_context=True, no_pm=True)
    async def ping(self, ctx):
        """
        Calcule le temps que met un message a faire l'aller/retour entre ton poste et le bot

        """
        self.log.info(
            ctx.message.author.display_name
            + " > "
            + ctx.message.channel.name
            + " : "
            + ctx.message.clean_content
        )

        try:
            timer = time.monotonic()
            msg_id = await ctx.send_msg(ctx, msg=":ping_pong: **PONG !!!**")

            timer = "%.2f" % (1000 * (time.monotonic() - timer))

            await ctx.edit_msg(
                msg_id,
                msg_id,
                msg="La balle revient après "
                + timer
                + "ms. \n :ping_pong: **PONG !!!** ",
            )
        except Exception as e:
            pass


def setup(bot):  # noqa D103
    bot.add_cog(Inspector())
