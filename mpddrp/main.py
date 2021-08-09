#!/usr/bin/env python3

import sys
from time import sleep
from datetime import timedelta
from platform import system as psys
from subprocess import call as oscall
import colorama
from mpd import MPDClient
from pypresence import Presence
from .parsing import get_config


def main():

    version = "1.1.1"
    colorama.init()

    config = get_config()

    mpdc = MPDClient()
    mpdc.timeout = int(config["General"]["MPDtimeout"])
    mpdc.idletimeout = int(config["General"]["MPDtimeout_idle"])
    try:
        mpdc.connect(config["General"]["MPDip"],
                     port=int(config["General"]["MPDport"]))
    except ConnectionRefusedError:
        print(f"{colorama.Fore.RED}ERROR!!! Either mpd isn't running or you have a mistake in your config. Fix ASAP! Sys.Exiting!{colorama.Style.RESET_ALL}")
        colorama.deinit()
        sys.exit(-1)

    rpc = Presence(710956455867580427)
    rpc.connect()

    if psys() == "Windows":
        oscall("cls", shell=False)
    else:
        oscall("clear", shell=False)

    print(f"{colorama.Fore.GREEN}MPDDRP v.{version} - https://github.com/AKurushimi/mpddrp{colorama.Style.RESET_ALL}")

    try:
        while True:

            statusout = mpdc.status()
            csout = mpdc.currentsong()

            if statusout["state"] != "stop":
                title = csout["title"]
                artist = csout["artist"]
                album = csout["album"]
                timevar = statusout["time"].split(":")
                timenow = str(timedelta(seconds=int(timevar[0])))
                timeall = str(timedelta(seconds=int(timevar[1])))

            if statusout["state"] == "play":
                rpc.update(details=title + " | " + album,
                           state=timenow + "/" + timeall + " | " + artist,
                           large_image="mpdlogo",
                           small_image="play",
                           small_text="Playing")

            elif statusout["state"] == "pause":
                rpc.update(details=title + " | " + album,
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
                sleep(1)

    except (KeyboardInterrupt, SystemExit, RuntimeError):
        rpc.clear()
        rpc.close()
        colorama.deinit()
        sys.exit(0)
