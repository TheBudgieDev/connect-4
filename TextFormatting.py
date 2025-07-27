"""
Module that contains the text formatting functions using ANSI colour codes.
"""

from enum import Enum

class Colours(Enum):
    """Enum for the ANSI colour codes"""
    BLACK = "30"
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    PURPLE = "35"
    CYAN = "36"
    WHITE = "37"


class Styles(Enum):
    """Enum for the ANSI style codes"""
    NORMAL = "0"
    BOLD = "1"
    UNDERLINE = "4"


class BGColours(Enum):
    """Enum for the ANSI background colour codes"""
    BLACK = ";40"
    RED = ";41"
    GREEN = ";42"
    YELLOW = ";43"
    BLUE = ";44"
    PURPLE = ";45"
    CYAN = ";46"
    WHITE = ";47"
    DEFAULT = ""


def format_text(text: str="", colour: Colours=Colours.WHITE, style: Styles=Styles.NORMAL, bg_colour: BGColours=BGColours.DEFAULT) -> str:
    """
    Returns a string of the ANSI colour code of the given text attributes

    Keyword Arguments:
        text (str): Text to format
        colour (Colours): Colour of the text
        style (str): Style of the text
        bg_colour (BGColours): Background colour of the text

    Returns:
        str: Ansi colour code of the given text attributes
    """

    return f"\033[{style.value};{colour.value}{bg_colour.value}m" + text + "\033[0;37m"