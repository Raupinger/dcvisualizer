import math

import pandas as pd
import plotly.express as px
import os
import json
def hoursminutescombine(a, b):
    return a + b * 60
def addstuff(a, b):
    return a + b
if __name__ == '__main__':
    combined = pd.Series([])
    channels = {}
    guilds = []
    for root, dirs, files  in os.walk("/home/florian/Downloads/package/messages"):
        for filename in files:
            if filename == "channel.json":
                with open(os.path.join(root, filename), 'r', encoding='UTF-8') as channelfile:
                    channeldata = json.load(channelfile)
                    if "guild" in channeldata:
                        guilds.append(channeldata["guild"])
                    if "guild" in channeldata and channeldata["guild"]["id"] == "378294922786242581":

                        print(channeldata["name"])
                        print(root)
                        with open(os.path.join(root, "messages.csv"), newline='') as csvfile:
                            data = pd.read_csv(csvfile, parse_dates=[1])["Timestamp"].dt.tz_convert('Europe/Berlin')
                            hours = data.dt.hour
                            minutes = data.dt.minute
                            prepared = minutes.combine(hours, hoursminutescombine).value_counts().sort_index()
                            prepared.index = prepared.index.map(lambda a: pd.Timedelta(seconds=(a*60)) + pd.to_datetime('1970/01/01'))
                            prepared.dropna()
                            print(prepared.index.max())
                            combined = prepared.combine(other=combined, func=addstuff, fill_value=0)

                            channels[channeldata["name"]] =prepared.rolling('60min').mean()
    #tail = combined.tail('60min')
    #tail.index = tail.index.map(lambda a: a - pd.to_datetime('1970/01/02'))
    #combined = combined.append(tail)
    # print(combined.head())
    channels["total"] = combined.rolling('60min').mean()
    print(combined.index[:0])
    print(pd.concat(channels, axis=1).head())
    finaldata = pd.concat(channels, axis=1)
    px.line(finaldata).show()
