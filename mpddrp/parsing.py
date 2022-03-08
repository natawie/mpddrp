#!/usr/bin/env python3

# /
#   mpddrp - MPD Discord Rich Presence
#   Copyright (C) 2022 Natalia Łotocka

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#                                                                          /

"""parses the config file"""

import sys
import platform
import subprocess
import os
import getpass
import json
import colorama
from .colourful_output import error


def get_config():
    """reads the config file and returns it as an object"""

    username = getpass.getuser()

    if platform.system() == "Windows":
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

    if os.path.exists(config_dir + "config.json"):
        with open(config_dir + "config.json", "r", encoding="utf-8") as configfile:
            config = json.loads(configfile.read())
            configfile.close()

            # impractical if more sections are going to be added... replace this when that happens
            for default_setting in default_config["General"]:
                for setting in config["General"]:
                    if config["General"][setting] == "":
                        error(f"ERROR!!! {setting} doesn't have a value assigned! Fix ASAP! Exiting!")
                        colorama.deinit()
                        sys.exit(1)
                    try:
                        if config["General"][default_setting]:
                            continue
                    except KeyError:
                        error(f"ERROR!!! Please add {default_setting} in your config file! Fix ASAP! Exiting!")
                        colorama.deinit()
                        sys.exit(1)
    else:
        subprocess.run(["mkdir", "-p" , f"{config_dir}"], shell=False, check=False)
        with open(config_dir + "config.json", "w", encoding="utf-8") as configfile:
            configfile.write(json.dumps(default_config, indent=4, sort_keys=True))
            configfile.close()
            config = default_config

    return config
