# Raven - UserBot


from asyncio import sleep

from telethon.errors import MessageDeleteForbiddenError, MessageNotModifiedError
from telethon.tl.custom import Message
from telethon.tl.types import MessageService

from core.setup import LOGS

# edit or reply


async def eor(
    event: Message, text=None, time=None, link_preview=False, edit_time=None, **args
):
    reply_to = event.reply_to_msg_id or event
    if event.out and not isinstance(event, MessageService):
        if edit_time:
            await sleep(edit_time)
        if args.get("file") and not event.media:
            await event.delete()
            ok = await event.client.send_message(
                event.chat_id,
                text,
                link_preview=link_preview,
                reply_to=reply_to,
                **args
            )

        else:
            try:
                ok = await event.edit(text, link_preview=link_preview, **args)
            except MessageNotModifiedError:
                ok = event
    else:
        ok = await event.client.send_message(
            event.chat_id, text, link_preview=link_preview, reply_to=reply_to, **args
        )

    if time:
        await sleep(time)
        return await ok.delete()
    event._eor = ok

    return ok


async def eod(event, text=None, **kwargs):
    kwargs["time"] = kwargs.get("time", 8)
    return await eor(event, text, **kwargs)


async def _try_delete(event):
    try:
        return await event.delete()
    except MessageDeleteForbiddenError:
        pass
    except BaseException as er:
        LOGS.error("Error while Deleting Message..")
        LOGS.exception(er)


setattr(Message, "eor", eor)
setattr(Message, "try_delete", _try_delete)
