from discordsweeper import makeDiscordMinesweeper
import subprocess
from dice import rollDie
from imdb_plugin import *
import requests 
import discord
from discord.ext import commands, tasks
import asyncio
import re
import json
import xml.etree.ElementTree as ET
from requests.exceptions import ReadTimeout
from pyquery import PyQuery as pq
import os
from pytube import Channel, YouTube
from datetime import datetime, timedelta
import time


def get_new_youtube_movies():
    print("getting new youtube movies")
    
    channels = [ t.strip() for t in open("/home/hd1/tetsuharu/JewD/youtube_channel_list.txt").readlines() ]
    print(f"getting new youtube movies for {len(channels)} channels")
    
    for chanid in channels:
        c = Channel(chanid)
        for url in c:
            y = YouTube(url)
            # check if it exists already?
            if not os.path.isdir(f"/home/hd1/tetsuharu/media/B Movies/{y.title}"):
                print(y.length/60/60)
                if y.length/60/60 > 1.0:
                    print(f"downloading {url} {y.title}")
                    subprocess.Popen(["/home/hd1/tetsuharu/bin/youdown", url])
                else:
                    print(f"not downloading {url} {y.title} ===> too small")
            else:
                print(f"not download {url} {y.title} ====> may have already been downloaded")

get_new_youtube_movies()


