__version__ = "1.0.1";
__author__ = "Franz Łotocki";
import pypresence as pp;
from mpd import MPDClient;
import time;
import datetime;
import platform;
import os;
import json;
import getpass;

username = getpass.getuser();

def clear():
    if ( platform.system() == 'Windows' ):
        os.system('cls');
    else:
        os.system('clear');

if ( platform.system() == 'Windows' ):
    if ( os.path.exists(f"C:\\Users\\{username}\\AppData\\Roaming\\mpddrp\\config") == True):
        configfile = open(f"C:\\Users\{username}\\AppData\\Roaming\\mpddrp\\config", "r");
        config = configfile.read();
        configfile.close();
        config = json.loads(config);
    else:
        os.system("mkdir ~\\AppData\\Roaming\\mpddrp");
        infile = {
                "MPDip": "localhost",
                "MPDport": "6600",
                "MPDtimeout": "10",
                "RPCid": "default"
        }
        configfile = open(f"C:\\Users\\{username}\\AppData\\Roaming\\mpddrp\\config", "w");
        configfile.write(json.dumps(infile));
        config = infile;
else:
    if ( os.path.exists(f"/home/{username}/.config/mpddrp/config") == True ):
        configfile = open(f"/home/{username}/.config/mpddrp/config", "r");
        config = configfile.read();
        configfile.close();
        config = json.loads(config);
    else:
        os.system("mkdir -p ~/.config/mpddrp/");
        infile = {
                "MPDip": "localhost",
                "MPDport": "6600",
                "MPDtimeout": "10",
                "RPCid": "default"
        }
        configfile = open(f"/home/{username}/.config/mpddrp/config", "w");
        configfile.write(json.dumps(infile));
        config = infile;

mpdc=MPDClient();
mpdc.timeout = int(config["MPDtimeout"]);
mpdc.idletimeout = None;
mpdc.connect(config["MPDip"], port=int(config["MPDport"]));

if (config["RPCid"] == "default"):
    client_id=710956455867580427;
else:
    client_id=int(config["RPCid"]);

RPC = pp.Presence(client_id);
RPC.connect();
if ( platform.system() == 'Windows' ):
    os.system('cls');
else:
    os.system('clear');
print("MPDDRP - github.com/PanKohnih/mpddrp");
try:
    while True:
        statusout = mpdc.status();
        csout = mpdc.currentsong();
        if (statusout["state"] == "pause"):
            title = csout["title"];
            artist = csout["artist"];
            album = csout["album"];
            RPC.update(details=title + " | " + album, state="Paused | " + artist, large_image="mpdlogo", small_image="pause", small_text="Paused");
        elif (statusout["state"] == "stop"):
            RPC.update(details="Stopped | MPDDRP", state="github.com/PanKohnih/mpddrp", large_image="mpdlogo", small_image="stop", small_text="Stopped");
        elif (statusout["state"] == "play"):
            title = csout["title"];
            artist = csout["artist"];
            album = csout["album"];
            timevar = statusout["time"].split(":");
            timenow = str(datetime.timedelta(seconds=int(timevar[0])));
            timeall = str(datetime.timedelta(seconds=int(timevar[1])));
            RPC.update(details=title + " | " + album, state=timenow + "/" + timeall + " | " + artist, large_image="mpdlogo", small_image="play", small_text="Playing");
        time.sleep(1);
except (KeyboardInterrupt, SystemExit):
    RPC.clear();
    RPC.close();
