# Raven - UserBot


import os
import platform
import sys
from logging import INFO, WARNING, FileHandler, StreamHandler, basicConfig, getLogger
from .config import HOSTED_ON

import contextlib
from telethon import __version__
from telethon.tl.alltlobjects import LAYER

from core.version import version


def _ask_input():
    # Ask for Input even on Vps and other platforms.
    def new_input(*args, **kwargs):
        raise EOFError(f"args={args}, kwargs={kwargs}")

    __builtins__["input"] = new_input


file = f"raven{sys.argv[6]}.log" if len(sys.argv) > 6 else "raven.log"

if os.path.exists(file):
    os.remove(file)

LOGS = getLogger("pyRvnLogs")
TelethonLogger = getLogger("Telethon")
TelethonLogger.setLevel(WARNING)

_ask_input()

_LOG_FORMAT = "%(asctime)s | %(name)s [%(levelname)s] : %(message)s"
basicConfig(
    format=_LOG_FORMAT,
    level=INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[FileHandler(file), StreamHandler()],
)

with contextlib.suppress(ImportError):
    import coloredlogs # type: ignore

    coloredlogs.install(level=None, logger=LOGS, fmt=_LOG_FORMAT)

LOGS.info(
    """
-----------------------------------
Starting Deployment
-----------------------------------
"""
)

LOGS.info(f"Python version - {platform.python_version()}")
LOGS.info(f"Telethon Version - {__version__} [Layer: {LAYER}]")
LOGS.info(f"Raven Version - {version} [{HOSTED_ON}] [{platform.system()}]")

try:
    from safety.tools import *     # type: ignore
except ImportError:
    LOGS.error("'safety' package not found!")
