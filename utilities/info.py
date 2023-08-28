# raven - UserBot


async def get_uinfo(e):
    user, data = None, None
    reply = await e.get_reply_message()
    data = e.pattern_match.group(1).strip()
    if reply:
        user = await reply.get_sender()
    else:
        ok = data.split(maxsplit=1)
        if len(ok) > 1:
            data = ok[1]
        try:
            user = await e.client.get_entity(await e.client.parse_id(ok[0]))
        except IndexError:
            pass
        except ValueError as er:
            await e.eor(str(er))
            return None, None
    return user, data

