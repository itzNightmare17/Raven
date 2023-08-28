# Raven - UserBot



import sys

import time
from .config import Var
from .setup import *
from .client.BaseClient import RavenClient
from .utils.base import validate_session, update_handlers
from database import udB
from .version import version
from .remote import rm

start_time = time.time()

LOGS.info("Connected to %s...", udB.name)

BOT_MODE = udB.get_config("BOTMODE")
DUAL_MODE = udB.get_config("DUAL_MODE")

USER_MODE = udB.get_config("USER_MODE")
if USER_MODE or BOT_MODE:
    DUAL_MODE = False

__token = udB.get_config("BOT_TOKEN")
if BOT_MODE and not __token:
    LOGS.critical('"BOT_TOKEN" not Found! Please add it, in order to use "BOTMODE"')
    sys.exit()
elif not BOT_MODE:
    raven_bot = RavenClient(
        validate_session(Var.SESSION, LOGS),
        app_version=version,
        device_model="Raven",
    )

asst = RavenClient("asst", bot_token=__token)

if BOT_MODE:
    raven_bot = asst
    if owner_id:= udB.get_config("OWNER_ID"):
        try:
            raven_bot.me = raven_bot.run_in_loop(
                raven_bot.get_entity(owner_id)
            )
        except Exception as er:
            LOGS.exception(er)

del __token

HNDLR = udB.get_key("HNDLR") or "."
DUAL_HNDLR = udB.get_key("DUAL_HNDLR") or "/"
SUDO_HNDLR = udB.get_key("SUDO_HNDLR") or HNDLR

for _ in ["HNDLR", "DUAL_HNDLR"]:
    udB.on(_, "change", update_handlers)
