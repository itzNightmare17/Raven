# Raven - UserBot


from localization import get_help

__doc__ = get_help("chats")

import contextlib
from telethon.errors import ChatAdminRequiredError as no_admin
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    DeleteChannelRequest,
    EditPhotoRequest,
    GetFullChannelRequest,
    UpdateUsernameRequest,
)
from utilities.converter import create_chat_photo
from telethon.tl.functions.messages import (
    CreateChatRequest,
    ExportChatInviteRequest,
    GetFullChatRequest,
)
from telethon.tl.types import (
    ChannelParticipantsKicked,
    User,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)

from .. import HNDLR, LOGS, asst, get_string, mediainfo, os, types, udB, raven_cmd


@raven_cmd(pattern="delchat", groups_only=True, fullsudo=True)
async def _(e):
    xx = await e.eor(get_string("com_1"))
    try:
        match = e.text.split(" ", maxsplit=1)[1]
        chat = await e.client.parse_id(match)
    except IndexError:
        chat = e.chat_id
    try:
        await e.client(DeleteChannelRequest(chat))
    except TypeError:
        return await xx.eor(get_string("chats_1"), time=10)
    except no_admin:
        return await xx.eor(get_string("chats_2"), time=10)
    await e.client.send_message(
        udB.get_config("LOG_CHANNEL"), get_string("chats_6").format(e.chat_id)
    )


@raven_cmd(
    pattern="getlink( (.*)|$)",
    groups_only=True,
    manager=True,
)
async def getlink_func(e):
    reply = await e.get_reply_message()
    match = e.pattern_match.group(1).strip()
    if reply and not isinstance(reply.sender, User):
        chat = await reply.get_sender()
    else:
        chat = await e.get_chat()
    if hasattr(chat, "username") and chat.username:
        return await e.eor(f"Username: @{chat.username}")
    request, usage, title, link = None, None, None, None
    if match:
        split = match.split(maxsplit=1)
        request = split[0] in ["r", "request"]
        title = "Created by Raven"
        if len(split) > 1:
            match = split[1]
            spli = match.split(maxsplit=1)
            if spli[0].isdigit():
                usage = int(spli[0])
            if len(spli) > 1:
                title = spli[1]
        elif not request:
            if match.isdigit():
                usage = int(match)
            else:
                title = match
        if request and usage:
            usage = 0
    if request or title:
        try:
            r = await e.client(
                ExportChatInviteRequest(
                    e.chat_id,
                    request_needed=request,
                    usage_limit=usage,
                    title=title,
                ),
            )
        except no_admin:
            return await e.eor(get_string("chats_2"), time=10)
        link = r.link
    else:
        if isinstance(chat, types.Chat):
            FC = await e.client(GetFullChatRequest(chat.id))
        elif isinstance(chat, types.Channel):
            FC = await e.client(GetFullChannelRequest(chat.id))
        else:
            return
        Inv = FC.full_chat.exported_invite
        if Inv and not Inv.revoked:
            link = Inv.link
    if link:
        return await e.eor(f"Link:- {link}")
    await e.eor("`Failed to getlink!\nSeems like link is inaccessible to you...`")


@raven_cmd(
    pattern="create (b|g|c)(?: |$)(.*)",
)
async def _(e):
    type_of_group = e.pattern_match.group(1).strip()
    group_name = e.pattern_match.group(2)
    username = None
    if " ; " in group_name:
        group_ = group_name.split(" ; ", maxsplit=1)
        group_name = group_[0]
        username = group_[1]
    xx = await e.eor(get_string("com_1"))
    if type_of_group == "b":
        try:
            r = await e.client(
                CreateChatRequest(
                    users=[asst.me.username],
                    title=group_name,
                ),
            )
            created_chat_id = r.chats[0].id
            result = await e.client(
                ExportChatInviteRequest(
                    peer=created_chat_id,
                ),
            )
            await xx.edit(
                get_string("chats_4").format(group_name, result.link),
                link_preview=False,
            )
        except Exception as ex:
            await xx.edit(str(ex))
    elif type_of_group in ["g", "c"]:
        try:
            r = await e.client(
                CreateChannelRequest(
                    title=group_name,
                    about=get_string("chats_5"),
                    megagroup=type_of_group != "c",
                )
            )

            created_chat_id = r.chats[0].id
            if username:
                await e.client(UpdateUsernameRequest(created_chat_id, username))
                result = f"https://t.me/{username}"
            else:
                result = (
                    await e.client(
                        ExportChatInviteRequest(
                            peer=created_chat_id,
                        ),
                    )
                ).link
            await xx.edit(
                get_string("chats_6").format(f"[{group_name}]({result})"),
                link_preview=False,
            )
        except Exception as ex:
            await xx.edit(str(ex))


# ---------------------------------------------------------------- #


@raven_cmd(
    pattern="setgpic( (.*)|$)", admins_only=True, manager=True, require="change_info"
)
async def _(rav):
    if not rav.is_reply:
        return await rav.eor("`Reply to a Media..`", time=5)
    match = rav.pattern_match.group(1).strip()
    if not rav.client._bot and match:
        try:
            chat = await rav.client.parse_id(match)
        except Exception as ok:
            return await rav.eor(str(ok))
    else:
        chat = rav.chat_id
    reply = await rav.get_reply_message()
    if reply.photo or reply.sticker or reply.video:
        replfile = await reply.download_media()
    elif reply.document and reply.document.thumbs:
        replfile = await reply.download_media(thumb=-1)
    else:
        return await rav.eor("Reply to a Photo or Video..")
    mediain = mediainfo(reply.media)
    cnfile = await create_chat_photo(replfile)

    file = await rav.client.upload_file(cnfile)
    try:
        isPhoto = cnfile.endswith(("jpg", "png"))
        file = types.InputChatUploadedPhoto(file=file if isPhoto else None, video=None if isPhoto else file)
        await rav.client(EditPhotoRequest(chat, file))
        await rav.eor("`Group Photo has Successfully Changed !`", time=5)
    except Exception as ex:
        LOGS.exception(ex)
        await rav.eor(f"Error occured.\n`{str(ex)}`", time=5)
    os.remove(replfile)
    with contextlib.suppress(FileNotFoundError):
        os.remove(cnfile)


@raven_cmd(
    pattern="delgpic( (.*)|$)", admins_only=True, manager=True, require="change_info"
)
async def _(rav):
    match = rav.pattern_match.group(1).strip()
    chat = match if not rav.client._bot and match else rav.chat_id
    try:
        await rav.client(EditPhotoRequest(chat, types.InputChatPhotoEmpty()))
        text = "`Removed Chat Photo..`"
    except Exception as E:
        text = str(E)
    return await rav.eor(text, time=5)


@raven_cmd(pattern="unbanall$", manager=True, admins_only=True, require="ban_users")
async def _(event):
    xx = await event.eor("Searching Participant Lists.")
    p = 0
    title = (await event.get_chat()).title
    async for i in event.client.iter_participants(
        event.chat_id,
        filter=ChannelParticipantsKicked,
        aggressive=True,
    ):
        try:
            await event.client.edit_permissions(event.chat_id, i, view_messages=True)
            p += 1
        except no_admin:
            pass
        except BaseException as er:
            LOGS.exception(er)
    await xx.eor(f"{title}: {p} unbanned", time=5)


@raven_cmd(
    pattern="rmusers( (.*)|$)",
    groups_only=True,
    admins_only=True,
    fullsudo=True,
)
async def rmusers_cmd(event):
    # TODO: Simplify and UPDATE
    xx = await event.eor(get_string("com_1"))
    input_str = event.pattern_match.group(1).strip()
    p, b, c, d, m, n, y, w, o, q, r = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    async for i in event.client.iter_participants(event.chat_id):
        kick_req = event.client.kick_participant(event.chat_id, i)

        p += 1  # Total Count
        if isinstance(i.status, UserStatusEmpty):
            if "empty" in input_str:
                with contextlib.suppress(BaseException):
                    await kick_req
                    c += 1
            else:
                y += 1
        elif isinstance(i.status, UserStatusLastMonth):
            if "month" in input_str:
                with contextlib.suppress(BaseException):
                    await kick_req
                    c += 1
            else:
                m += 1
        elif isinstance(i.status, UserStatusLastWeek):
            if "week" in input_str:
                with contextlib.suppress(BaseException):
                    await kick_req
                    c += 1
            else:
                w += 1
        elif isinstance(i.status, UserStatusOffline):
            if "offline" in input_str:
                with contextlib.suppress(BaseException):
                    await kick_req
                    c += 1
            else:
                o += 1
        elif isinstance(i.status, UserStatusOnline):
            if "online" in input_str:
                with contextlib.suppress(BaseException):
                    await kick_req
                    c += 1
            else:
                q += 1
        elif isinstance(i.status, UserStatusRecently):
            if "recently" in input_str:
                with contextlib.suppress(BaseException):
                    await kick_req
                    c += 1
            else:
                r += 1
        if i.bot:
            if "bot" in input_str:
                with contextlib.suppress(BaseException):
                    await kick_req
                    c += 1
            else:
                b += 1
        elif i.deleted:
            if "deleted" in input_str:
                with contextlib.suppress(BaseException):
                    await kick_req
                    c += 1
            else:
                d += 1
        elif i.status is None:
            if "none" in input_str:
                with contextlib.suppress(BaseException):
                    await kick_req
                    c += 1
            else:
                n += 1
    if input_str:
        required_string = f"**>> Kicked** `{c} / {p}` **users**\n\n"
    else:
        required_string = f"**>> Total** `{p}` **users**\n\n"
    required_string += f"  `{HNDLR}rmusers deleted`  **••**  `{d}`\n"
    required_string += f"  `{HNDLR}rmusers empty`  **••**  `{y}`\n"
    required_string += f"  `{HNDLR}rmusers month`  **••**  `{m}`\n"
    required_string += f"  `{HNDLR}rmusers week`  **••**  `{w}`\n"
    required_string += f"  `{HNDLR}rmusers offline`  **••**  `{o}`\n"
    required_string += f"  `{HNDLR}rmusers online`  **••**  `{q}`\n"
    required_string += f"  `{HNDLR}rmusers recently`  **••**  `{r}`\n"
    required_string += f"  `{HNDLR}rmusers bot`  **••**  `{b}`\n"
    required_string += f"  `{HNDLR}rmusers none`  **••**  `{n}`"
    await xx.eor(required_string)
