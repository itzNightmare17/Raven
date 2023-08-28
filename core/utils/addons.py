# Raven - UserBot


from importlib import util
from sys import modules

from core import HNDLR, LOGS, asst, udB, raven_bot
from core.config import Var
from core.decorators import _supporter as config
from core.decorators._assistant import asst_cmd, callback, in_pattern
from core.decorators._decorators import raven_cmd
from core.decorators._supporter import Config, admin_cmd, sudo_cmd
from core.decorators._wrappers import eod, eor
from database._core import CMD_HELP as HELP

# for addons

configPaths = [
    "ub",
    "var",
    "support",
    "userbot",
    "telebot",
    "fridaybot",
    "uniborg.util",
    "telebot.utils",
    "userbot.utils",
    "userbot.events",
    "userbot.config",
    "fridaybot.utils",
    "fridaybot.Config",
    "userbot.uniborgConfig",
]


def load_addons(plugin_name):
    import core
    import modules as m

    base_name = plugin_name.split("/")[-1].split("\\")[-1].replace(".py", "")
    if base_name.startswith("__"):
        return
    name = plugin_name.replace("/", ".").replace("\\", ".").replace(".py", "")
    spec = util.spec_from_file_location(name, plugin_name)
    mod = util.module_from_spec(spec)
    for path in configPaths:
        modules[path] = config
    modules["pyUltroid"] = core
    modules["plugins"] = m
    mod.LOG_CHANNEL = udB.get_config("LOG_CHANNEL")
    mod.udB = udB
    mod.asst = asst
    mod.tgbot = asst
    mod.raven_bot = raven_bot
    mod.ub = raven_bot
    mod.bot = raven_bot
    mod.raven = raven_bot
    mod.borg = raven_bot
    mod.telebot = raven_bot
    mod.jarvis = raven_bot
    mod.friday = raven_bot
    mod.eod = eod
    mod.edit_delete = eod
    mod.LOGS = LOGS
    mod.in_pattern = in_pattern
    mod.hndlr = HNDLR
    mod.handler = HNDLR
    mod.HNDLR = HNDLR
    mod.CMD_HNDLR = HNDLR
    mod.Config = Config
    mod.Var = Var
    mod.eor = eor
    mod.edit_or_reply = eor
    mod.asst_cmd = asst_cmd
    mod.raven_cmd = raven_cmd
    mod.on_cmd = raven_cmd
    mod.callback = callback
    mod.Redis = udB.get_key
    mod.admin_cmd = admin_cmd
    mod.sudo_cmd = sudo_cmd
    mod.HELP = HELP
    mod.CMD_HELP = HELP

    spec.loader.exec_module(mod)
    modules[name] = mod
    doc = modules[name].__doc__.format(i=HNDLR) if modules[name].__doc__ else ""
    if "Addons" in HELP.keys():
        update_cmd = HELP
        try:
            update_cmd.update({base_name: doc})
        except BaseException:
            pass
    else:
        try:
            HELP[base_name] = doc
        except BaseException:
            pass
