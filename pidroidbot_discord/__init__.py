"""
Package interface.

This is the init package interface.
"""
__version__ = "1.0.3"


# Project
from pidroidbot_discord import launcher
from pidroidbot_discord.launcher import _, __, bot, log


if __name__ == "__main__":
    launcher.main()
