from discordsweeper import makeDiscordMinesweeper
import math
import subprocess
from dice import rollDie
from imdb_plugin import *
import requests 
import discord
from discord import FFmpegPCMAudio
from discord.utils import get
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
from flights import getMatchedFlights
import random
from dalle import gen_image, gen_image_grid
from io import BytesIO

import aiohttp
import markov
import news_feeds
import bmovie_title_markov
import bmovie_summary_markov
from types import ModuleType




import glob


def asyncget(url):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: requests.get(url, verify=False, timeout=60*5).json())


intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
intents.message_content = True

new_movies_added = []

#bot = commands.Bot(command_prefix='$', help_command=None, intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)



previous_server_restart = datetime.now()

@bot.event
async def on_ready():
    print( 'We have logged in as {0.user}'.format(bot))

conversation_mode = False
dalle_channel = 989705155446448178

dalle_prompts = []
dalle_users = []
dalle_images = {}

@bot.event
async def on_reaction_add(reaction, user):
    global dalle_channel
    print("on reaction add")
    print(reaction)
    print(reaction.message)
    print(reaction.message.attachments)
    if reaction.message.channel.id != dalle_channel:
        return
    attachments = reaction.message.attachments
    if len(attachments) > 0:
        img = attachments[0]
        print("img",img)
        async with aiohttp.ClientSession() as session:
            async with session.get(str(img)) as resp:
                msg = reaction.message.content
                msg = re.sub(r"^<[^>]+> \"","", re.sub(r"\"$","", msg))
                n = datetime.now()
                datestr = n.strftime("%Y%m%d%H%M")
                with open(f"saved/{datestr} {msg}.png","wb") as f:
                    f.write(await resp.read())
        

voice = None



@bot.event
async def on_message(message):
    global conversation_mode
    global dalle_prompts, dalle_users, dalle_images, dalle_channel
    print("message >> " + message.content)
    if message.author == bot.user:
        return



    

current_movie = None
@tasks.loop(seconds=5)
async def check_current_movie():
    global current_movie
    #CHANNEL_ID = 802733321138077756 # bad-movies
    CHANNEL_ID = 949958580440805377 # mute
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        return
    print('check_current_movie')
    r = requests.get("https://bodygen.re:8081/get_current_movie", verify=False)
    r = r.content.decode('utf-8')
    print('current movie: ',r)
    if current_movie == r:
        return
    print('new movie')
    if current_movie != None:
        print('sending message')
        s = await channel.send("Current playing:\n" + r)
        print(s)
    print('sent message')
    current_movie = r



#@tasks.loop(seconds=10)
@tasks.loop(hours=1)
async def change_stream_bot_name():
    print('changing streambot nickname')
    noop_chance = 0.8
    if random.random() < noop_chance: return
    botid = 877264289411514458
    names = "Sony,Toshiba,JVC,Mitsubishi,Panasonic,Hitachi,Zenith,Samsung,RCA,Sharp,Philips,Sanyo,Magnavox,GE".split(",")
    new_name = random.choice(names)

    member = get(bot.get_all_members(), id=botid)
    if not member: return

    print('member', member)   
    await member.edit(nick=new_name)
    with open(f"tv_icons/{new_name}.png", "rb") as image:
        print(f"member updating image to tv_icons/{new_name}.png")
        await member.edit(avatar=image.read())
    



# import all modules/
for t in glob.glob('modules/*.py'):
   __import__(t.replace('/','.')[0:-3])
modules = __import__('modules')

# register all module endpoints
for k, m in modules.__dict__.items():
    if isinstance(m, ModuleType):
        m.register(bot)
        if 'on_message' in m.__dict__:
            on_message_handlers.append(m.on_message)
        if 'on_reaction_add' in m.__dict__:
            on_reaction_add_handlers.append(m.on_reaction_add)





#  check_torrents.start()
#check_dead_meat.start()
#check_current_movie.start()
#get_new_youtube_movies.start()
#   change_stream_bot_name.start()
#dalle_the_news.start()
#markov_the_news.start()
#markov_the_npr_news.start()
#    notify_new_movies.start()

#bot.run('OTQ0Nzk5MjE5MDk5NzY2ODc1.YhG21w.wecQSj-OQDsq00LW6-gn1goUFvM')
bot.run('OTQ0Nzk5MjE5MDk5NzY2ODc1.Gru9vD.o5RMpayPhc5jfQIHtSHAd5wjN6kR-FB6-34Dcs')


