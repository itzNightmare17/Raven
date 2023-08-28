# Raven - UserBot


"""
✘ Commands Available -

• `{i}addsudo`
    Add Sudo Users by replying to user or using <space> separated userid(s)

• `{i}delsudo`
    Remove Sudo Users by replying to user or using <space> separated userid(s)

• `{i}listsudo`
    List all sudo users.
"""

from telethon.tl.types import User

from core import raven_bot
from core.decorators import get_sudos, is_sudo
from utilities.helper import inline_mention

from .. import get_string, udB, raven_cmd


@raven_cmd(pattern="addsudo( (.*)|$)", fullsudo=True)
async def addsudo_func(rav):
    inputs = rav.pattern_match.group(1).strip()
    if rav.reply_to_msg_id:
        replied_to = await rav.get_reply_message()
        id_ = replied_to.sender_id
        name = await replied_to.get_sender()
    elif inputs:
        id_ = inputs
        try:
            name = await rav.client.get_entity(inputs)
        except BaseException:
            name = None
    elif rav.is_private:
        id_ = rav.chat_id
        name = await rav.get_chat()
    else:
        return await rav.eor(get_string("sudo_1"), time=5)
    if name and isinstance(name, User) and (name.bot or name.verified):
        return await rav.eor(get_string("sudo_4"))
    name = inline_mention(name) if name else f"`{id_}`"
    if id_ == raven_bot.uid:
        mmm = get_string("sudo_2")
    elif is_sudo(id_):
        mmm = f"{name} `is already a SUDO User ...`"
    else:
        udB.set_key("SUDO", "True")
        key = get_sudos()
        key.append(id_)
        udB.set_key("SUDOS", key)
        mmm = f"**Added** {name} **as SUDO User**"
    await rav.eor(mmm, time=5)


@raven_cmd(pattern="delsudo( (.*)|$)", fullsudo=True)
async def delsudo_func(rav):
    inputs = rav.pattern_match.group(1).strip()
    if rav.reply_to_msg_id:
        replied_to = await rav.get_reply_message()
        id_ = replied_to.sender_id
        name = await replied_to.get_sender()
    elif inputs:
        id_ = inputs
        try:
            name = await rav.client.get_entity(id_)
        except BaseException:
            name = None
    elif rav.is_private:
        id_ = rav.chat_id
        name = await rav.get_chat()
    else:
        return await rav.eor(get_string("sudo_1"), time=5)
    name = inline_mention(name) if name else f"`{id_}`"
    if not is_sudo(id_):
        mmm = f"{name} `wasn't a SUDO User ...`"
    else:
        key = get_sudos()
        key.remove(id_)
        udB.set_key("SUDOS", key)
        mmm = f"**Removed** {name} **from SUDO User(s)**"
    await rav.eor(mmm, time=5)


@raven_cmd(
    pattern="listsudo$",
)
async def listsudo_func(rav):
    sudos = get_sudos()
    if not sudos:
        return await rav.eor(get_string("sudo_3"), time=5)
    msg = ""
    for i in sudos:
        try:
            name = await rav.client.get_entity(i)
        except BaseException:
            name = None
        if name:
            msg += f"• {inline_mention(name)} ( `{i}` )\n"
        else:
            msg += f"• `{i}` -> Invalid User\n"
    m = udB.get_key("SUDO")
    if m is not True:
        m = "[False](https://graph.org/Ultroid-04-06)"
    return await rav.eor(
        f"**SUDO MODE : {m}\n\nList of SUDO Users :**\n{msg}", link_preview=False
    )
