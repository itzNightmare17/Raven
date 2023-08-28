# /usr/bin/python3
# Raven - UserBot

# Standalone file for facilitating local deploys.

import os

a = r"""

 ██████╗   █████╗  ██╗   ██╗ ███████╗ ███╗   ██╗
 ██╔══██╗ ██╔══██╗ ██║   ██║ ██╔════╝ ████╗  ██║
 ██████╔╝ ███████║ ██║   ██║ █████╗   ██╔██╗ ██║
 ██╔══██╗ ██╔══██║ ╚██╗ ██╔╝ ██╔══╝   ██║╚██╗██║
 ██║  ██║ ██║  ██║  ╚████╔╝  ███████╗ ██║ ╚████║
 ╚═╝  ╚═╝ ╚═╝  ╚═╝   ╚═══╝   ╚══════╝ ╚═╝  ╚═══╝

"""


def start():
    clear_screen()
    check_for_py()

    print(f"{a}\n\n")
    print("Welcome to Raven, lets start setting up!\n\n")
    print("Cloning the repository...\n\n")
    os.system("rm -rf Raven")
    os.system("git clone https://github.com/itzNightmare17/Raven")
    print("\n\nDone")
    os.chdir("Raven")
    print_with_clear(a, "\n\nLet's start!\n")
    # generate session if needed.
    sessionisneeded = input(
        "Do you want to generate a new session, or have an old session string? [generate/skip]",
    )
    if sessionisneeded == "generate":
        gen_session()
    elif sessionisneeded != "skip":
        print(
            'Please choose "generate" to generate a session string, or "skip" to pass on.\n\nPlease run the script again!',
        )
        exit(0)

    # start bleck megik
    print("\n\nLets start entering the variables.\n\n")
    varrs = [
        "API_ID",
        "API_HASH",
        "SESSION",
        "REDIS_URI",
        "REDIS_PASSWORD",
    ]
    all_done = "# Raven Environment Variables.\n# Do not delete this file.\n\n"
    for i in varrs:
        all_done += do_input(i)
    print_with_clear(a, "\n\nHere are the things you've entered.\nKindly check.")
    print(all_done)
    isitdone = input("\n\nIs it all correct? [y/n]")
    if isitdone == "y" or isitdone != "n":
        # raven
        f = open(".env", "w")
        f.write(all_done)
    else:
        print("Oh, let's redo these then.")
        start()
    print_with_clear(
        "\nCongrats. All done!\nTime to start the bot!",
        "\nInstalling requirements... This might take a while...",
    )
    os.system("pip3 install --no-cache-dir -r requirements.txt")
    ask = input(
        "Enter 'yes/y' to Install other requirements, required for local deployment."
    )
    if ask.lower().startswith("y"):
        print("Started Installing...")
        os.system(
            "pip3 install --no-cache-dir -r resources/extras/optional-requirements.txt"
        )
    else:
        print("Skipped!")
    print_with_clear(a, "\nStarting Raven...")
    os.system("sh startup")


def print_with_clear(arg0, arg1):
    clear_screen()
    print(arg0)
    print(arg1)


def do_input(var):
    val = input(f"Enter your {var}: ")
    return f"{var}={val}\n"


def clear_screen():
    # clear screen
    _ = os.system("clear") if os.name == "posix" else os.system("cls")


def check_for_py():
    print(
        "Please make sure you have python installed. \nGet it from http://python.org/\n\n",
    )
    try:
        ch = int(
            input(
                "Enter Choice:\n1. Continue, python is installed.\n2. Exit and install python.\n",
            ),
        )
    except BaseException:
        print("Please run the script again, and enter the choice as a number!!")
        exit(0)
    if ch == 1:
        pass
    elif ch == 2:
        print("Please install python and continue!")
        exit(0)
    else:
        print("Weren't you taught how to read? Enter a choice!!")
        return


def gen_session():
    print("\nProcessing...")
    # raven
    os.system("python3 resources/session/ssgen.py")


start()
