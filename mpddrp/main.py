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

"""main file"""

import sys
import time
import datetime
import platform
import subprocess
import colorama
import mpd
import pypresence
from .parsing import get_config
from .colourful_output import success, error, info


def construct_details(title, album):
    """constructs the text for the details field in rpc.update() providing length checks"""

    details = title + " | " + album
    if len(details) > 127:
        # info("song title + album was too long to display... switching to only song title")
        if len(title) > 127:
            # info("song title was too long to display... song title was cut")
            details = title[:len(title) - 127 - 3] + "..."
        details = title
    return details

def attempt_mpd_connection(mpdc, config):
    """tries to connect to an mpd server"""

    try:
        mpdc.connect(config["General"]["MPDip"],
                     port=int(config["General"]["MPDport"]))
    except ConnectionRefusedError:
        error("ERROR!!! Either mpd isn't running or you have a mistake in your config. Fix ASAP!")
        info("Waiting 5 seconds then attempting to connect again")
        try:
            time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            colorama.deinit()
            sys.exit(0)
        attempt_mpd_connection(mpdc, config)

def attempt_rpc_connection(rpc):
    """tries to connect to discord with rich presence"""
    try:
        rpc.connect()
    except (ConnectionRefusedError, pypresence.exceptions.DiscordError, pypresence.exceptions.DiscordNotFound):
        error("ERROR!!! Either Discord isn't running or there's a problem with your connection")
        info("Waiting 5 seconds then attempting to connect again")
        try:
            time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            colorama.deinit()
            sys.exit(0)
        attempt_rpc_connection(rpc)

def main():
    """main"""

    version = "1.1.2"
    colorama.init()

    config = get_config()

    mpdc = mpd.MPDClient()
    mpdc.timeout = int(config["General"]["MPDtimeout"])
    mpdc.idletimeout = int(config["General"]["MPDtimeout_idle"])

    attempt_mpd_connection(mpdc, config)

    rpc = pypresence.Presence(710956455867580427)
    attempt_rpc_connection(rpc)

    if platform.system() == "Windows":
        subprocess.run("cls", shell=False, check=False)
    else:
        subprocess.run("clear", shell=False, check=False)

    success(f"mpddrp v{version} - https://github.com/AKurushimi/mpddrp")

    while True:
        try:
            statusout = mpdc.status()
            csout = mpdc.currentsong()

            if statusout["state"] != "stop":
                title = csout["title"]
                artist = csout["artist"]
                album = csout["album"]
                timevar = statusout["time"].split(":")
                timenow = str(datetime.timedelta(seconds=int(timevar[0])))
                timeall = str(datetime.timedelta(seconds=int(timevar[1])))

            if statusout["state"] == "play":
                rpc.update(details=construct_details(title, album),
                           state=artist,
                           large_image="mpdlogo",
                           small_image="play",
                           small_text=timenow + "/" + timeall)

            elif statusout["state"] == "pause":
                rpc.update(details=construct_details(title, album),
                           state="Paused | " + artist,
                           large_image="mpdlogo",
                           small_image="pause",
                           small_text="Paused")

            elif statusout["state"] == "stop":
                rpc.update(details="Stopped | MPD",
                           state="   ",
                           large_image="mpdlogo",
                           small_image="stop",
                           small_text="Stopped")
            time.sleep(1)
        except mpd.base.ConnectionError:
            attempt_mpd_connection(mpdc, config)
        except (pypresence.exceptions.InvalidID, pypresence.exceptions.DiscordNotFound):
            attempt_rpc_connection(rpc)
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            rpc.clear()
            rpc.close()
            colorama.deinit()
            sys.exit(0)
