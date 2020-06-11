import pypresence as pp;
from mpd import MPDClient;
import time;
import datetime;

mpdc=MPDClient();
mpdc.timeout = 10;
mpdc.idletimeout = None;
mpdc.connect("localhost", port=6600);
client_id= ;
RPC = pp.Presence(client_id);
RPC.connect();
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
