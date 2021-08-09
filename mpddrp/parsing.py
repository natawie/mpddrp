#!/usr/bin/env python3

import sys
from platform import system as psys
from subprocess import call as oscall
from os import path
from getpass import getuser
from json import loads, dumps
import colorama


def get_config():

    platform = psys()
    username = getuser()

    if platform == "Windows":
        config_dir = f"C:\\Users\\{username}\\AppData\\Roaming\\mpddrp\\"
    else:
        config_dir = f"/home/{username}/.config/mpddrp/"

    default_config = {
        "General": {
            "MPDip": "localhost",
            "MPDport": 6600,
            "MPDtimeout": 10,
            "MPDtimeout_idle": 0
        }
    }

    if path.exists(config_dir + "config.json"):
        with open(config_dir + "config.json", "r") as configfile:
            config = loads(configfile.read())
            configfile.close()

            for default_setting in default_config["General"]:
                for setting in config["General"]:
                    if config["General"][setting] == "":
                        print(f"{colorama.Fore.RED}ERROR!!! {setting} doesn't have a value assigned! Fix ASAP! Sys.Exiting!{colorama.Style.RESET_ALL}")
                        colorama.deinit()
                        sys.exit(-1)
                        try:
                            if config["General"][default_setting]:
                                continue
                        except KeyError:
                            print(f"{colorama.Fore.RED}ERROR!!! Please add {default_setting} in your config file! Fix ASAP! Sys.Exiting!{colorama.Style.RESET_ALL}")
                            colorama.deinit()
                            sys.exit(-1)
    else:
        oscall(f"mkdir -p {config_dir}", shell=False)
        with open(config_dir + "config.json", "w") as configfile:
            configfile.write(dumps(default_config, indent=4, sort_keys=True))
            configfile.close()
            config = default_config

    return config
