# Raven - UserBot


from contextlib import suppress

from database import udB

from ._wrappers import eod, eor

# ----------------------------------------------#


def should_allow_sudos():
    return udB.get_key("SUDO")


def get_sudos() -> list:
    return udB.get_key("SUDOS") or []  # type: ignore


def is_sudo(userid):
    return userid in get_sudos()


def owner_and_sudos():
    return [udB.get_config("OWNER_ID"), *get_sudos()]


def _parse(key):
    with suppress(TypeError):
        return int(key)
    return key


def fullsudos():
    fullsudos = []
    if sudos := udB.get_key("FULLSUDO"):
        fullsudos.extend(str(sudos).split())
    owner = udB.get_config("OWNER_ID")
    if owner and owner not in fullsudos:
        fullsudos.append(owner)
    return list(map(_parse, filter(lambda id: id, fullsudos)))

# ------------------------------------------------ #