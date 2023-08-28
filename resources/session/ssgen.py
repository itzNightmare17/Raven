#!/usr/bin/python3
# Raven - UserBot

import os
from time import sleep

RAVEN = r"""

 ██████╗   █████╗  ██╗   ██╗ ███████╗ ███╗   ██╗
 ██╔══██╗ ██╔══██╗ ██║   ██║ ██╔════╝ ████╗  ██║
 ██████╔╝ ███████║ ██║   ██║ █████╗   ██╔██╗ ██║
 ██╔══██╗ ██╔══██║ ╚██╗ ██╔╝ ██╔══╝   ██║╚██╗██║
 ██║  ██║ ██║  ██║  ╚████╔╝  ███████╗ ██║ ╚████║
 ╚═╝  ╚═╝ ╚═╝  ╚═╝   ╚═══╝   ╚══════╝ ╚═╝  ╚═══╝

"""


def spinner(x):
    if x == "tele":
        print("Checking if Telethon is installed...")
    else:
        print("Checking if Pyrogram is installed...")
    for _ in range(3):
        for frame in r"-\|/-\|/":
            print("\b", frame, sep="", end="", flush=True)
            sleep(0.1)


def clear_screen():
    # https://www.tutorialspoint.com/how-to-clear-screen-in-python#:~:text=In%20Python%20sometimes%20we%20have,screen%20by%20pressing%20Control%20%2B%20l%20.
    if os.name == "posix":
        os.system("clear")
    else:
        # for windows platfrom
        os.system("cls")


def get_api_id_and_hash():
    print(
        "Get your API ID and API HASH from my.telegram.org or @ScrapperRoBot to proceed.\n\n",
    )
    try:
        API_ID = int(input("Please enter your API ID: "))
    except ValueError:
        print("APP ID must be an integer.\nQuitting...")
        exit(0)
    API_HASH = input("Please enter your API HASH: ")
    return API_ID, API_HASH


def telethon_session():
    try:
        spinner("tele")

        x = "\bFound an existing installation of Telethon...\nSuccessfully Imported.\n\n"
    except ImportError:
        print("Installing Telethon...")
        os.system("pip install -U telethon")

        x = "\bDone. Installed and imported Telethon."
    clear_screen()
    print(RAVEN)
    print(x)

    # the imports

    from telethon.errors.rpcerrorlist import (
        ApiIdInvalidError,
        PhoneNumberInvalidError,
        UserIsBotError,
    )
    from telethon.sessions import StringSession
    from telethon.sync import TelegramClient

    API_ID, API_HASH = get_api_id_and_hash()

    # logging in
    try:
        with TelegramClient(StringSession(), API_ID, API_HASH) as raven:
            print("Generating a string session for • R A V E N •")
            try:
                raven.send_message(
                    "me",
                    f"**RAVEN** `SESSION`:\n\n`{raven.session.save()}`\n\n**Do not share this anywhere!**",
                )
                print(
                    "Your SESSION has been generated. Check your Telegram saved messages!"
                )
                return
            except UserIsBotError:
                print("You are trying to Generate Session for your Bot's Account?")
                print("Here is That!\n{raven.session.save()}\n\n")
                print("NOTE: You can't use that as User Session..")
    except ApiIdInvalidError:
        print(
            "Your API ID/API HASH combination is invalid. Kindly recheck.\nQuitting..."
        )
        exit(0)
    except ValueError:
        print("API HASH must not be empty!\nQuitting...")
        exit(0)
    except PhoneNumberInvalidError:
        print("The phone number is invalid!\nQuitting...")
        exit(0)
    except Exception as er:
        print("Unexpected Error Occurred while Creating Session")
        print(er)
        print("If you think It as a Bug, Report to @UltroidSupportChat.\n\n")


def pyro_session():
    try:
        spinner("pyro")
        from pyrogram import Client

        x = "\bFound an existing installation of Pyrogram...\nSuccessfully Imported.\n\n"
    except BaseException:
        print("Installing Pyrogram...")
        os.system("pip install pyrogram tgcrypto")
        x = "\bDone. Installed and imported Pyrogram."
    clear_screen()
    print(RAVEN)
    print(x)

    # generate a session
    API_ID, API_HASH = get_api_id_and_hash()
    print("Enter phone number when asked.\n\n")
    try:
        with Client(":memory:", api_id=API_ID, api_hash=API_HASH) as pyro:
            ss = pyro.export_session_string()
            pyro.send_message(
                "me",
                f"`{ss}`\n\nAbove is your Pyrogram Session String for @TheRaven. **DO NOT SHARE it.**",
            )
            print("Session has been sent to your saved messages!")
            exit(0)
    except Exception as er:
        print(
            "Unexpected error occurred while creating session, make sure to validate your inputs."
        )
        print(er)


def main():
    clear_screen()
    print(RAVEN)
    try:
        type_of_ss = int(
            input(
                "\nRaven supports both telethon as well as pyrogram sessions.\n\nWhich session do you want to generate?\n1. Telethon Session.\n2. Pyrogram Session.\n\nEnter choice:  "
            )
        )
    except Exception as e:
        print(e)
        exit(0)
    if type_of_ss == 1:
        telethon_session()
    elif type_of_ss == 2:
        pyro_session()
    else:
        print("Invalid choice.")
    x = input("Run again? (Y/n)")
    if x.lower() in ["y", "yes"]:
        main()
    else:
        exit(0)


main()
