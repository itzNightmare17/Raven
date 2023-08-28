# /usr/bin/python3
# raven - UserBot


from datetime import datetime
from os import path, system
from time import sleep

try:
    from colorama import Back, Fore, Style
except ModuleNotFoundError:
    print("Installing colorama...")
    system("pip install -q colorama")
    from colorama import Back, Fore, Style


# clear screen
def clear():
    system("clear")


MANDATORY_REQS = [
    "https://github.com/New-dev0/Telethon/archive/Cartoon.zip",
    "gitpython",
    "enhancer",
    "telegraph",
    "requests",
    "python-decouple",
    "aiohttp",
]

OPT_PACKAGES = {
    "bs4": "Used for site-scrapping (used in commands like - .gadget and many more)",
    "yt-dlp": "Used for Youtuble Related Downloads...",
    "youtube-search-python": "Used for youtube video search..",
    "pillow": "Used for Image-Conversion related task. (size - approx 50mb ) (required for kang, convert and many more.)",
    "psutil": "Used for .usage command.",
    "lottie": "Used for animated sticker related conversion.",
    "apscheduler": "Used in autopic/nightmode (scheduling tasks.)",
    # "git+https://github.com/1danish-00/google_trans_new.git": "Used for translation purposes.",
}

APT_PACKAGES = ["ffmpeg", "neofetch", "mediainfo"]

DISCLAIMER_TEXT = ""

COPYRIGHT = f"©️ TeamRaven {datetime.now().year}"

HEADER = f"""
╔╗ ╔╗╔╗  ╔╗            ╔╗
║║ ║║║║ ╔╝╚╗           ║║
║║ ║║║║ ╚╗╔╝╔═╗╔══╗╔╗╔═╝║
║║ ║║║║  ║║ ║╔╝║╔╗║╠╣║╔╗║
║╚═╝║║╚╗ ║╚╗║║ ║╚╝║║║║╚╝║
╚═══╝╚═╝ ╚═╝╚╝ ╚══╝╚╝╚══╝\n
"""

INFO_TEXT = f"""
{Fore.GREEN}# Important points to know.

{Fore.YELLOW}1. This script will just install basic requirements because of which some command whose requirements are missing won't work. You can view all optional requirements in (./resources/extras/optional-requirements.txt)

2. You can install that requirement whenever you want with 'pip install' (a very basic python+bash knowledge is required.)

3. Some of the plugins are disabled for 'Termux Users' to save resources (by adding in EXCLUDE_OFFICIAL).
   - Read More - https://t.me/UltroidUpdates/36
   - Also, way to enable the disabled plugins is mentioned in that post.

   # Disabled Plugins Name
    -    autocorrect    -     compressor
    -    Gdrive         -     instagram
    -    nsfwfilter     -     glitch
    -    pdftools       -     writer
    -    youtube        -     megadl
    -    autopic        -     nightmode
    -    blacklist      -     forcesubscribe

4. You can't use 'VCBOT' on Termux.

5. You can't use 'MongoDB' on Termux (Android).
{Fore.RESET}
* Hope you are smart enought to understand.
* Enter 'A' to Continue, 'E' to Exit..\n
"""


def ask_and_wait(text, header: bool = False):
    if header:
        text = with_header(text)
    print(text + "\nPress 'ANY Key' to Continue or 'Ctrl+C' to exit...\n")
    input("")


def with_header(text):
    return Fore.MAGENTA + HEADER + Fore.RESET + "\n\n" + text


def yes_no_apt():
    yes_no = input("").strip().lower()
    if yes_no in ["yes", "y"]:
        return True
    elif yes_no in ["no", "n"]:
        return False
    print("Invalid Input\nRe-Enter: ")
    return yes_no_apt()


def ask_process_info_text():
    strm = input("").lower().strip()
    if strm == "e":
        print("Exiting...")
        exit(0)
    elif strm != "a":
        print("Invalid Input")
        print("Enter 'A' to Continue or 'E' to exit...")
        ask_process_info_text()


def ask_process_apt_install():
    strm = input("").lower().strip()
    if strm == "e":
        print("Exiting...")
        exit(0)
    elif strm == "a":
        for apt in APT_PACKAGES:
            print(f"* Do you want to install '{apt}'? [Y/N] ")
            if yes_no_apt():
                print(f"Installing {apt}...")
                system(f"apt install {apt} -y")
            else:
                print(f"- Discarded {apt}.\n")
    elif strm == "i":
        names = " ".join(APT_PACKAGES)
        print("Installing all apt-packages...")
        system(f"apt install {names} -y")
    elif strm != "s":
        print("Invalid Input\n* Enter Again...")
        ask_process_apt_install()


def ask_and_wait_opt():
    strm = input("").strip().lower()
    if strm == "e":
        print("Exiting...")
        exit(0)
    elif strm == "a":
        for opt in OPT_PACKAGES.keys():
            print(
                f"* {Fore.YELLOW}Do you want to install '{opt}'? [Y/N]\n- {OPT_PACKAGES[opt]}"
            )
            if yes_no_apt():
                print(f"Installing {opt}...")
                system(f"pip install -q {opt}")
            else:
                print(f"{Fore.YELLOW}- Discarded {opt}.\n")
    elif strm == "i":
        names = " ".join(OPT_PACKAGES.keys())
        print(f"{Fore.YELLOW}Installing all packages...")
        system(f"pip install -q {names}")
    elif strm != "s":
        print("Invalid Input\n* Enter Again...")
        ask_and_wait_opt()


def ask_make_env():
    strm = input("").strip().lower()
    if strm in ["yes", "y"]:
        print(f"{Fore.YELLOW}* Creating .env file..")
        with open(".env", "a") as file:
            for var in ["API_ID", "API_HASH", "SESSION", "REDIS_URI", "REDIS_PASSWORD"]:
                inp = input(f"Enter {var}\n- ")
                file.write(f"{var}={inp}\n")
        print("* Created '.env' file successfully! 😃")

    else:
        print("OK!")


# ------------------------------------------------------------------------------------------ #

clear()

print(
    f"""
{Fore.BLACK}{Back.WHITE}{HEADER}{Style.RESET_ALL}
{Fore.GREEN}- RAVEN Termux Installation -
  The Main Aim of this script is to deploy Raven with basic requirements and save your phone resources.
{Fore.RESET}

{COPYRIGHT}
    """
)
print("Press 'Any Key' to continue...")
input("")
clear()

print(with_header(INFO_TEXT))
ask_process_info_text()

clear()

print(with_header("Installing Mandatory requirements..."))
all_ = " ".join(MANDATORY_REQS)
system(f"pip install -q {all_}")

clear()
print(
    with_header(
        f"\n{Fore.GREEN}# Moving toward Installing Apt-Packages{Fore.RESET}\n\n"
    )
)
print("---Enter---")
print(" - A = 'Ask Y/N for each'.")
print(" - I = 'Install all'")
print(" - S = 'Skip Apt installation.'")
print(" - E = Exit.\n")
ask_process_apt_install()

clear()
print(
    with_header(
        f"""
{Fore.YELLOW}# Installing other non mandatory requirements.
(You can Install them, if you want command using them to work!){Fore.RESET}

{'\n- '.join(list(OPT_PACKAGES.keys()))}


Enter [ A = Ask for each, I = Install all, S = Skip, E = Exit]"""
    )
)
ask_and_wait_opt()

print(f"\n{Fore.RED}#EXTRA Features...\n")
print(f"{Fore.YELLOW}* Do you want to get Raven Logs in Colors? [Y/N] ")
inp = input("").strip().lower()
if inp in ["yes", "y"]:
    print(f"{Fore.GREEN}*Spoking the Magical Mantras*")
    system("pip install -q coloredlogs")
else:
    print("Skipped!")

clear()
if not path.exists(".env"):
    print(with_header("# Do you want to move toward creating .env file ? [y/N] "))
    ask_make_env()

clear()
print(with_header(f"\n{Fore.GREEN}You are all Done! 🥳"))
sleep(0.2)
print(f"Use './raven start' to try running Raven.{Fore.RESET}")
sleep(0.5)
print(
    "\nYou can head over to @UltroidSupportChat, if you get stuck somewhere, and need help."
)
sleep(0.5)
print("\nMade with ❤️ by @TeamRaven...")

system("pip uninstall -q colorama -y")
