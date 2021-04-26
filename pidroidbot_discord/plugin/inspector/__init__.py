"""Inspector contains all main's tools for administrators."""

# TODO : plugins
#   a réorganiser en plugins/<nom plugins>/main.py et default_conf
#   revoir fonctionnement core.py

# Project
from pidroidbot_discord.module.pluginmanager.core import Core


class Inspector(Core):
    """
    Plugin Inspector.

    Do nothing yet
    """


def setup(bot):  # noqa D103
    bot.add_cog(Inspector(bot))
