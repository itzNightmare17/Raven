# Raven - UserBot


from localization import get_help

__doc__ = get_help("admins")

from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import EditAdminRequest, GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.types import InputMessagesFilterPinned
from telethon.utils import get_display_name

from core import HNDLR
from core.decorators._wrappers import eod, eor
from database.helpers import DEVLIST
from utilities.admins import ban_time
from utilities.helper import inline_mention
from utilities.info import get_uinfo

from .. import LOGS, get_string, types, raven_cmd


@raven_cmd(
    pattern="promote( (.*)|$)",
    admins_only=True,
    manager=True,
    require="add_admins",
    fullsudo=True,
)
async def prmte(rav):
    xx = await rav.eor(get_string("com_1"))
    user, rank = await get_uinfo(rav)
    if not rank:
        rank = "Admin"
    FullRight = False
    if not user:
        return await xx.edit(get_string("pro_1"))
    if rank.split()[0] == "-f":
        try:
            rank = rank.split(maxsplit=1)[1]
        except IndexError:
            rank = "Admin"
        FullRight = True
    try:
        if FullRight:
            await rav.client(
                EditAdminRequest(rav.chat_id, user.id, rav.chat.admin_rights, rank)
            )
        else:
            await rav.client.edit_admin(
                rav.chat_id,
                user.id,
                invite_users=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                manage_call=True,
                title=rank,
            )
        await eod(
            xx, get_string("pro_2").format(inline_mention(user), rav.chat.title, rank)
        )
    except Exception as ex:
        return await xx.edit(f"`{ex}`")


@raven_cmd(
    pattern="demote( (.*)|$)",
    admins_only=True,
    manager=True,
    require="add_admins",
    fullsudo=True,
)
async def dmote(rav):
    xx = await rav.eor(get_string("com_1"))
    user, rank = await get_uinfo(rav)
    if not rank:
        rank = "Not Admin"
    if not user:
        return await xx.edit(get_string("de_1"))
    try:
        await rav.client.edit_admin(
            rav.chat_id,
            user.id,
            invite_users=None,
            ban_users=None,
            delete_messages=None,
            pin_messages=None,
            manage_call=None,
            title=rank,
        )
        await eod(xx, get_string("de_2").format(inline_mention(user), rav.chat.title))
    except Exception as ex:
        return await xx.edit(f"`{ex}`")


@raven_cmd(
    pattern="ban( (.*)|$)",
    admins_only=True,
    manager=True,
    require="ban_users",
    fullsudo=True,
)
async def bban(rav):
    something = await get_uinfo(rav)
    if not something:
        return
    user, reason = something
    if not user:
        return await eod(rav, get_string("ban_1"))
    if user.id in DEVLIST:
        return await eod(rav, get_string("ban_2"))
    try:
        await rav.client.edit_permissions(rav.chat_id, user.id, view_messages=False)
    except UserIdInvalidError:
        return await eod(rav, get_string("adm_1"))
    except BadRequestError:
        return await eod(rav, get_string("ban_3"))
    senderme = inline_mention(await rav.get_sender())
    userme = inline_mention(user)
    text = get_string("ban_4").format(userme, senderme, rav.chat.title)
    if reason:
        text += get_string("ban_5").format(reason)
    await eod(rav, text)


@raven_cmd(
    pattern="unban( (.*)|$)",
    admins_only=True,
    manager=True,
    require="ban_users",
    fullsudo=True,
)
async def uunban(rav):
    xx = await rav.eor(get_string("com_1"))
    if rav.text[1:].startswith("unbanall"):
        return
    something = await get_uinfo(rav)
    if not something:
        return
    user, reason = something
    if not user:
        return await xx.edit(get_string("unban_1"))
    try:
        await rav.client.edit_permissions(rav.chat_id, user.id, view_messages=True)
    except UserIdInvalidError:
        return await eod(rav, get_string("adm_1"))
    except BadRequestError:
        return await xx.edit(get_string("adm_2"))
    sender = inline_mention(await rav.get_sender())
    text = get_string("unban_3").format(inline_mention(user), sender, rav.chat.title)
    if reason:
        text += get_string("ban_5").format(reason)
    await xx.edit(text)


@raven_cmd(
    pattern="kick( (.*)|$)",
    manager=True,
    require="ban_users",
    fullsudo=True,
)
async def kck(rav):
    if "kickme" in rav.text:
        return
    if rav.is_private:
        return await rav.eor("`Use this in Group/Channel.`", time=5)
    ml = rav.text.split(" ", maxsplit=1)[0]
    xx = await rav.eor(get_string("com_1"))
    something = await get_uinfo(rav)
    if not something:
        return
    user, reason = something
    if not user:
        return await xx.edit(get_string("adm_1"))
    if user.id in DEVLIST:
        return await xx.edit(get_string("kick_2"))
    if getattr(user, "is_self", False):
        return await xx.edit(get_string("kick_3"))
    try:
        await rav.client.kick_participant(rav.chat_id, user.id)
    except BadRequestError as er:
        LOGS.info(er)
        return await xx.edit(get_string("kick_1"))
    except Exception as e:
        LOGS.exception(e)
        return
    text = get_string("kick_4").format(
        inline_mention(user), inline_mention(await rav.get_sender()), rav.chat.title
    )
    if reason:
        text += get_string("ban_5").format(reason)
    await xx.edit(text)


@raven_cmd(
    pattern="tban( (.*)|$)",
    admins_only=True,
    manager=True,
    require="ban_users",
    fullsudo=True,
)
async def tkicki(e):
    huh = e.text.split()
    inputt = None
    try:
        tme = huh[1]
    except IndexError:
        return await e.eor(get_string("adm_3"), time=15)
    try:
        inputt = huh[2]
    except IndexError:
        if e.reply_to_msg_id:
            inputt = (await e.get_reply_message()).sender_id
    if not inputt:
        return await e.eor(get_string("tban_1"))
    userid = await e.client.parse_id(inputt)
    try:
        user = await e.client.get_entity(userid)
    except Exception as ex:
        return await eor(e, f"`{ex}`")
    try:
        bun = ban_time(tme)
        await e.client.edit_permissions(
            e.chat_id, user.id, until_date=bun, view_messages=False
        )
        await eod(
            e,
            get_string("tban_2").format(inline_mention(user), e.chat.title, tme),
            time=15,
        )
    except Exception as m:
        return await e.eor(str(m))


@raven_cmd(pattern="pin$", manager=True, require="pin_messages", fullsudo=True)
async def pin(msg):
    if not msg.is_reply:
        return await msg.eor(get_string("pin_1"))
    me = await msg.get_reply_message()
    if me.is_private:
        text = "`Pinned.`"
    else:
        text = f"Pinned [This Message]({me.message_link}) !"
    try:
        await msg.client.pin_message(msg.chat_id, me.id, notify=False)
    except BadRequestError:
        return await msg.eor(get_string("adm_2"))
    except Exception as e:
        return await msg.eor(f"**ERROR:**`{e}`")
    await msg.eor(text)


@raven_cmd(
    pattern="unpin($| (.*))",
    manager=True,
    require="pin_messages",
    fullsudo=True,
)
async def unp(rav):
    xx = await rav.eor(get_string("com_1"))
    ch = (rav.pattern_match.group(1).strip()).strip()
    msg = None
    if rav.is_reply:
        msg = rav.reply_to_msg_id
    elif ch != "all":
        return await xx.edit(get_string("unpin_1").format(HNDLR))
    try:
        await rav.client.unpin_message(rav.chat_id, msg)
    except BadRequestError:
        return await xx.edit(get_string("adm_2"))
    except Exception as e:
        return await xx.edit(f"**ERROR:**`{e}`")
    await xx.edit("`Unpinned!`")


@raven_cmd(pattern="purge( (.*)|$)", manager=True, require="delete_messages")
async def fastpurger(purg):
    match = purg.pattern_match.group(1).strip()
    try:
        ABC = purg.text[6]
    except IndexError:
        ABC = None
    if ABC and purg.text[6] in ["m", "a"]:
        return
    if not purg._client._bot and (
        (match)
        or (purg.is_reply and (purg.is_private or isinstance(purg.chat, types.Chat)))
    ):
        p = 0
        async for msg in purg.client.iter_messages(
            purg.chat_id,
            limit=int(match) if match else None,
            min_id=purg.reply_to_msg_id if purg.is_reply else None,
        ):
            await msg.delete()
            p += 0
        return await purg.eor(f"Purged {p} Messages! ", time=5)
    if not purg.reply_to_msg_id:
        return await purg.eor(get_string("purge_1"), time=10)
    try:
        await purg.client.delete_messages(
            purg.chat_id, list(range(purg.reply_to_msg_id, purg.id))
        )

    except Exception as er:
        LOGS.info(er)
    await purg.eor("__Fast purge complete!__", time=5)


@raven_cmd(
    pattern="purgeme( (.*)|$)",
)
async def fastpurgerme(purg):
    if num := purg.pattern_match.group(1).strip():
        try:
            nnt = int(num)
        except BaseException:
            await purg.eor(get_string("com_3"), time=5)
            return
        mp = 0
        async for mm in purg.client.iter_messages(
            purg.chat_id, limit=nnt, from_user="me"
        ):
            await mm.delete()
            mp += 1
        await purg.eor(f"Purged {mp} Messages!", time=5)
        return
    elif not purg.reply_to_msg_id:
        return await purg.eor(
            "`Reply to a message to purge from or use it like ``purgeme <num>`",
            time=10,
        )
    chat = await purg.get_input_chat()
    msgs = []
    async for msg in purg.client.iter_messages(
        chat,
        from_user="me",
        min_id=purg.reply_to_msg_id,
    ):
        msgs.append(msg)
    if msgs:
        await purg.client.delete_messages(chat, msgs)
    await purg.eor(
        "__Fast purge complete!__\n**Purged** `" + str(len(msgs)) + "` **messages.**",
        time=5,
    )


@raven_cmd(
    pattern="purgeall$",
)
async def _(e):
    if not e.is_reply:
        return await eod(
            e,
            get_string("purgeall_1"),
        )

    msg = await e.get_reply_message()
    name = msg.sender
    try:
        await e.client.delete_messages(e.chat_id, from_user=msg.sender_id)
        await e.eor(get_string("purgeall_2").format(name.first_name), time=5)
    except Exception as er:
        return await e.eor(str(er), time=5)


@raven_cmd(pattern="pinned", manager=True, groups_only=True)
async def djshsh(event):
    chat = await event.get_chat()
    if isinstance(chat, types.Chat):
        FChat = await event.client(GetFullChatRequest(chat.id))
    elif isinstance(chat, types.Channel):
        FChat = await event.client(GetFullChannelRequest(chat.id))
    else:
        return
    msg_id = FChat.full_chat.pinned_msg_id
    if not msg_id:
        return await event.eor(get_string("pinned_1"))
    msg = await event.client.get_messages(chat.id, ids=msg_id)
    if msg:
        await event.eor(get_string("pinned_2").format(msg.message_link))


@raven_cmd(
    pattern="listpinned$",
)
async def get_all_pinned(event):
    x = await event.eor(get_string("com_1"))
    chat_id = (str(event.chat_id)).replace("-100", "")
    chat_name = get_display_name(event.chat)
    a = ""
    c = 1
    async for i in event.client.iter_messages(
        event.chat_id, filter=InputMessagesFilterPinned
    ):
        if i.message:
            t = " ".join(i.message.split()[:4])
            txt = f"{t}...."
        else:
            txt = "Go to message."
        a += f"{c}. <a href=https://t.me/c/{chat_id}/{i.id}>{txt}</a>\n"
        c += 1

    if c == 1:
        m = f"<b>The pinned message in {chat_name}:</b>\n\n"
    else:
        m = f"<b>List of pinned message(s) in {chat_name}:</b>\n\n"

    if not a:
        return await eor(x, get_string("listpin_1"), time=5)

    await x.edit(m + a, parse_mode="html")
