# Raven - UserBot

from . import *

import contextlib
import os
import sys
import time

from utilities.helper import bash, time_formatter, check_update
from .utils.funcs import process_main, load_plugins
from telethon.errors import SessionRevokedError

# Option to Auto Update On Restarts..
# TODO: UPDATE_ON_RESTART

raven_bot.me.phone = None

if not raven_bot.me.bot:
    udB.set_key("OWNER_ID", raven_bot.me.id)

LOGS.info("Initialising...")

if not udB.get_config("BOT_TOKEN"):
    with rm.get("autobot", helper=True) as mod:
        raven_bot.run_in_loop(mod.autopilot())


if HOSTED_ON == "heroku":
    rm._http_import("heroku", "core/heroku.py", helper=True)

raven_bot.run_in_loop(load_plugins())
raven_bot.loop.create_task(process_main())

with contextlib.suppress(BaseException):
    cleanup_cache()

LOGS.info(
    f"Took {time_formatter((time.time() - start_time) * 1000)} to start • R A V E N •"
)
LOGS.info(
    """
            ----------------------------------------------------------------------
                Raven has been deployed! Visit @TheRaven for updates!!
            ----------------------------------------------------------------------
"""
)
try:
    asst.run()
except SessionRevokedError:
    LOGS.info(f"Assistant [@{asst.me.username}]'s session was revoked!")

    # shift loop to bot
    raven_bot.run()
