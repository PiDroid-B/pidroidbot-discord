"""All tools about string manipulation."""

# Standard Library
from textwrap import TextWrapper


def wrap(text: str, width=80, indent=2):
    """Wrap text by length into array of texts wich indent for each new line."""
    wrapper = TextWrapper(width=width, subsequent_indent=" " * indent)
    return wrapper.wrap(text)
