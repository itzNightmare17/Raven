from random import choice

from database import udB

from .base import KeyManager

DEVLIST = [
    1953828896,  # @bad_oreo
]


def get_random_color():
    return choice(
        [
            "DarkCyan",
            "DeepSkyBlue",
            "DarkTurquoise",
            "Cyan",
            "LightSkyBlue",
            "Turquoise",
            "MediumVioletRed",
            "Aquamarine",
            "Lightcyan",
            "Azure",
            "Moccasin",
            "PowderBlue",
        ]
    )
