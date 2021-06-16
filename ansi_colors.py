# File:        ansi_colors.py
# Authors:     Bhavyai Gupta, Brandon Attai
# Description: Source code of the class Color providing attributes for coloring text output


class Color:
    """
    Class to contain variables to hold the ANSI codes for coloring text output

    Attributes:
        red (str):          ANSI sequence for bright red
        green (str):        ANSI sequence for bright green
        yellow (str):       ANSI sequence for yellow
        blue (str):         ANSI sequence for bight blue
        magenta (str):      ANSI sequence for bright magenta
        cyan (str):         ANSI sequence for cyan
        reset (str):        ANSI sequence for reset/normal
    """

    red = "\033[0;91m"
    green = "\033[0;92m"
    yellow = "\033[0;33m"
    blue = "\033[0;94m"
    magenta = "\033[0;95m"
    cyan = "\033[0;36m"
    reset = "\033[0m"
