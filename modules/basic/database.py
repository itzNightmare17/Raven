# Raven - UserBot


"""
• **DataBase Commands, do not use if you don't know what it is.**

• `{i}setdb key | value`
    Set Value in Database.
    e.g :
    `{i}setdb hi there`
    `{i}setdb hi there | raven here`
    `{i}setdb --extend variable value` or `{i}setdb -e variable value` to add the value to the exiting values in db.

• `{i}getdb key`
    Get Key from DB.

• `{i}deldb key`
    Delete Key from DB.

• `{i}rendb old keyname | new keyname`
    Update Key Name
"""

import re

from .. import eor, get_string, udB, raven_cmd, LOGS


async def _get_cmd(x, varname):
    val = udB.get_key(varname)
    if val is not None:
        return await x.eor(f"**Key** - `{varname}`\n**Value**: `{val}`")
    await x.eor( "No such key!", time=5)


@raven_cmd(pattern="setdb( (.*)|$)", fullsudo=True)
async def _(rav):
    match = rav.pattern_match.group(1).strip()
    if not match:
        return await rav.eor("Provide key and value to set!")
    try:
        delim = " " if re.search("[|]", match) is None else " | "
        data = match.split(delim, maxsplit=1)
        if data[0] in ["--extend", "-e"]:
            data = data[1].split(maxsplit=1)
            val = udB.get_key(data[0])
            if isinstance(val, str):
                data[1] = f"{val} {data[1]}"
            elif isinstance(val, list):
                val.append(data[1])
                data[1] = val
        udB.set_key(data[0], data[1])
        await rav.eor(
            f"**DB Key Value Pair Updated\nKey :** `{data[0]}`\n**Value :** `{data[1]}`"
        )

    except BaseException as er:
        LOGS.exception(er)
        await rav.eor(get_string("com_7"))


@raven_cmd(pattern="(del|get)db( (.*)|$)", fullsudo=True)
async def _(rav):
    _cmd = rav.pattern_match.group(1)
    key = rav.pattern_match.group(2).strip()
    if not key:
        return await rav.eor("Give me a key name to delete!", time=5)
    if _cmd == "get":
        return await _get_cmd(rav, key)
    _ = key.split(maxsplit=1)
    try:
        if _[0] == "-m":
            for key in _[1].split():
                k = udB.del_key(key)
            key = _[1]
            k = 0
        else:
            k = udB.del_key(key)
        if k == 0:
            return await rav.eor("`No Such Key.`")
        await rav.eor(f"`Successfully deleted key {key}`")
    except BaseException as er:
        LOGS.exception(er)
        await rav.eor(get_string("com_7"))


@raven_cmd(pattern="rendb( (.*)|$)", fullsudo=True)
async def _(rav):
    match = rav.pattern_match.group(1).strip()
    if not match:
        return await rav.eor("`Provide Keys name to rename..`")
    delim = " " if re.search("[|]", match) is None else " | "
    data = match.split(delim)
    if udB.get_key(data[0]):
        try:
            udB.rename(data[0], data[1])
            await eor(
                rav,
                f"**DB Key Rename Successful\nOld Key :** `{data[0]}`\n**New Key :** `{data[1]}`",
            )

        except BaseException:
            await rav.eor(get_string("com_7"))
        return
    await rav.eor("`No such key`")


@raven_cmd(pattern="getkeys", fullsudo=True)
async def getkeys_cmd(rav):
    keys = sorted(udB.keys())
    msg = "".join(
        f"• `{i}`" + "\n"
        for i in keys
        if not i.isdigit() and not i.startswith(("-", "_", "GBAN_REASON_"))
    )

    await rav.eor(f"**List of DB Keys :**\n{msg}")
