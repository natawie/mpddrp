#!/usr/bin/env python3

from pypresence import Presence;
from mpd import MPDClient;
from time import sleep;
from datetime import timedelta;
from .parsing import GetConfig;
from .termcolors import TermColors;
from platform import system as psys;
from os import system as ossys;
from sys import exit;

def main():

    VERSION = "1.1.0";

    config = GetConfig();

    mpdc = MPDClient();
    mpdc.timeout = int(config["General"]["MPDtimeout"]);
    mpdc.idletimeout = int(config["General"]["MPDtimeout_idle"]);
    try:
        mpdc.connect(config["General"]["MPDip"], port=int(config["General"]["MPDport"]));
    except ConnectionRefusedError:
        print(f"{TermColors.ERROR}ERROR!!! Either mpd isn't running or you have a mistake in the config. Fix ASAP! Exiting!{TermColors.END}");
        exit(-1);

    RPC = Presence(710956455867580427);
    RPC.connect();

    if (psys() == "Windows"):
        ossys("cls");
    else:
        ossys("clear");

    print(f"{TermColors.WORKS}MPDDRP v.{VERSION} - https://github.com/AKurushimi/mpddrp{TermColors.END}");

    try:
        while True:

            statusout = mpdc.status();
            csout = mpdc.currentsong();

            if (statusout["state"] != "stop"):
                title = csout["title"];
                artist = csout["artist"];
                album = csout["album"];
                timevar = statusout["time"].split(":");
                timenow = str(timedelta(seconds=int(timevar[0])));
                timeall = str(timedelta(seconds=int(timevar[1])));

            if (statusout["state"] == "pause"):
                RPC.update(details=title + " | " + album, state="Paused | " + artist, large_image="mpdlogo", small_image="pause", small_text="Paused");
            elif (statusout["state"] == "stop"):
                RPC.update(details="Stopped | MPD", state="   ", large_image="mpdlogo", small_image="stop", small_text="Stopped");
            elif (statusout["state"] == "play"):
                RPC.update(details=title + " | " + album, state=timenow + "/" + timeall + " | " + artist, large_image="mpdlogo", small_image="play", small_text="Playing");
                sleep(1);

    except (RuntimeError):
        pass;
    except (KeyboardInterrupt, SystemExit):
        RPC.clear();
        RPC.close();
        exit(0);
