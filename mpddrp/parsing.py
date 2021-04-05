#!/usr/bin/env python3

from platform import system as psys;
from os import system as ossys;
from os import path;
from sys import exit;
from getpass import getuser;
from json import loads, dumps;
from .termcolors import TermColors;

def GetConfig():

    platform = psys();
    username = getuser();

    if (platform == "Windows"):
        config_dir = f"C:\\Users\\{username}\\AppData\\Roaming\\mpddrp\\";
    else:
        config_dir = f"/home/{username}/.config/mpddrp/";

    default_config = {
    "General": {
        "MPDip": "localhost",
        "MPDport": 6600,
        "MPDtimeout": 10,
        "MPDtimeout_idle": 0
        }
    }

    if (path.exists(config_dir + "config.json")):
        configfile = open(config_dir + "config.json", "r");
        config = loads(configfile.read());
        configfile.close();

        for default_setting in default_config["General"]:
            for setting in config["General"]:
                if (config["General"][setting] == ""):
                    print(f"{TermColors.ERROR}ERROR!!! {setting} doesn't have a value assigned! Fix ASAP! Exiting!{TermColors.END}")
                    exit(-1);
                try:
                    if (config["General"][default_setting]):
                        continue;
                except KeyError:
                    print(f"{TermColors.ERROR}ERROR!!! Please add {default_setting} in your config file! Fix ASAP! Exiting!{TermColors.END}");
                    exit(-1);
    else:
        ossys(f"mkdir -p {config_dir}");
        configfile = open(config_dir + "config.json", "w");
        configfile.write(dumps(default_config, indent=4, sort_keys=True));
        configfile.close();
        config = default_config;

    return config;
