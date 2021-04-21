import math
import sys

import pandas as pd
import plotly.express as px
import os
import json

def hoursminutescombine(a, b):
    return a + b * 60
def addstuff(a, b):
    return a + b
if __name__ == '__main__':
    rootpath = ""
    while not os.path.isdir(rootpath):
        rootpath = input("Enter root of discord data: ") + "/messages"
    timezone = input("Enter time Zone, empty for UTC (this wont be checked): ") or "UTC"

    combined = pd.Series([])
    channels = {}
    channellist = []
    guilds = {}
    guildlist = []
    for root, dirs, files in os.walk(rootpath):
        for filename in files:
            if filename == "channel.json":
                with open(os.path.join(root, filename), 'r', encoding='UTF-8') as channelfile:
                    channeldata = json.load(channelfile)
                    if "guild" in channeldata:
                        channellist.append(channeldata)
                        guilds[channeldata["guild"]["id"]] = channeldata["guild"]
    selection = None
    i = 0;
    for guildid in guilds:
        print("%d: %s"%(i + 1, guilds[guildid]["name"]))
        guildlist.append(guilds[guildid])
        i += 1
    while selection == None:
        try:
            selection = channellist[int(input("Select Guild Nr.: "))]["guild"]["id"]
        except:
            ()
    print("calculating...")
    for channel in channellist:
        if channel["guild"]["id"] == selection:
            with open(os.path.join(rootpath, channel["id"], "messages.csv"), newline='') as csvfile:
                try:
                    data = pd.read_csv(csvfile, parse_dates=[1])["Timestamp"].dt.tz_convert(timezone)
                    hours = data.dt.hour
                    minutes = data.dt.minute
                    prepared = minutes.combine(hours, hoursminutescombine).value_counts().sort_index()
                    prepared.index = prepared.index.map(
                        lambda a: pd.Timedelta(seconds=(a * 60)) + pd.to_datetime('1970/01/01'))
                    prepared.dropna()
                    # print(prepared.index.max())
                    combined = prepared.combine(other=combined, func=addstuff, fill_value=0)

                    channels[channeldata["name"]] = prepared.rolling('60min').mean()
                except:
                    print("couldn't parse data for channel " + channel["name"] + " cause: " + str(sys.exc_info()[0]))
                    print(sys.exc_info()[0])
    channels["total"] = combined.rolling('60min').mean()
    finaldata = pd.concat(channels, axis=1)
    px.line(finaldata).show()
    print("done")
