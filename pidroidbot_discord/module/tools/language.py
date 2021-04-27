"""Manage all i18n features."""
# Standard Library
import gettext
import logging

# Project
from pidroidbot_discord.const import LANG_DIR


def load_language(lang):
    """
    Load locales from requested language, default english.

    :param lang: requested language, coming from locales/ (i.e. : fr_FR)
    :type lang: string
    :return: None
    """
    _ = gettext.gettext
    __ = gettext.ngettext

    log = logging.getLogger("main.language")

    if lang != "en_UK":
        try:
            traduction = gettext.translation(
                "messages",
                localedir=LANG_DIR,
                languages=[lang],
                fallback=False,
            )
            traduction.install()
            _ = traduction.gettext
            __ = traduction.ngettext
        except FileNotFoundError:
            log.debug(f"Language {lang} not found. English used as default language")
    return _, __
