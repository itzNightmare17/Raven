# Raven - UserBot
#
#   To Install Other USERBOTs plugin Support
#
#   RAVEN Don't Need This Stuffs


import os
import traceback

from telethon import events, types

from core import *
from core.config import Config
from core.decorators._decorators import compile_pattern, raven_cmd
from core.decorators._wrappers import eod, eor
from database._core import LIST

from . import get_sudos  # ignore: pylint

ALIVE_NAME = raven_bot.me.first_name
BOTLOG_CHATID = BOTLOG = udB.get_config("LOG_CHANNEL")


bot = borg = catub = friday = raven_bot
catub.cat_cmd = raven_cmd # type: ignore

black_list_chats = udB.get_key("BLACKLIST_CHATS")


def admin_cmd(pattern=None, func=None, **args):
    args["func"] = lambda e: not e.via_bot_id and func
    args["chats"] = black_list_chats
    args["blacklist_chats"] = True
    args["outgoing"] = True
    args["forwards"] = False
    if pattern:
        args["pattern"] = compile_pattern(pattern, HNDLR)
        file = os.path.basename(traceback.extract_stack(limit=2)[0].filename)[:-3]
        if LIST.get(file) is None:
            LIST[file] = []
        LIST[file].append(pattern)
    return events.NewMessage(**args)


friday_on_cmd = admin_cmd
register = command = raven_cmd

def sudo_cmd(allow_sudo=True, pattern=None, func=None, **args):
    args["func"] = lambda e: not e.via_bot_id and e.sender_id in get_sudos() and func
    args["chats"] = black_list_chats
    args["blacklist_chats"] = True
    args["forwards"] = False
    if pattern:
        args["pattern"] = compile_pattern(pattern, SUDO_HNDLR)
    if allow_sudo:
        args["incoming"] = True
    return events.NewMessage(**args)


edit_or_reply = eor
edit_delete = eod

CMD_HNDLR = HNDLR
