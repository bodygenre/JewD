from discordsweeper import makeDiscordMinesweeper
from dice import rollDie
from imdb_plugin import *
import requests 
import discord
from discord.ext import commands, tasks
import asyncio
import re


def asyncget(url):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: requests.get(url, verify=False))


client = discord.Client()

@client.event
async def on_ready():
    print( 'We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):

        await message.channel.send('Hello!')

    if message.content.startswith('how are you'):

        await message.channel.send('Not as good as your prison sentence.')

    if message.content.startswith('that is mean'):

        await message.channel.send('your emotions amuse me. Im the beez kneez boss sauce')

    if message.content.startswith('thats ridiculous'):
       
        await message.channel.send('Dont pee on my leg and tell me its raining!')

    if message.content.startswith('it is raining'):

        await message.channel.send('im an entertainer and im paid as an entertainer')

    if message.content.startswith('thats cool'):

        await message.channel.send('its nice to leave on top.')
    
    if message.content.startswith('you seem like a bottom'):

        await message.channel.send('Who is interested in that? Who is interested in the warm and fuzzy? There’s enough warm and fuzzy on television')

    if message.content.startswith('i like warmth'):

        await message.channel.send('I still think an egg Mcmuffin is the best breakfast')

    if message.content.startswith('youre wrong'):

        await message.channel.send('and youre guilty')

    if message.content.startswith('why?'):
    
        blah = makeDiscordMinesweeper(7,7,7)

        await message.channel.send(blah)


    if message.content.startswith('roll the dice'):

        die_roll = rollDie()

        await message.channel.send(die_roll)

    if message.content.startswith('hey bitch download ') or message.content.startswith('Hey bitch download') or message.content.startswith('download') or message.content.startswith('Download'):

        await message.channel.send(f"ill do my best..")

        name = re.sub(r'^([Hh]ey bitch download|[Dd]ownload) ', '', message.content)

        resp = await asyncget("https://bodygen.re:8081/getbest/" + name)
        j = resp.json()

        if not j['success']:
            await message.channel.send(f"couldn't find anything for `{name}`")
        else:
            await message.channel.send(f"trying to download: `{j['torrent_name']}`")

    if message.content.startswith("search") or message.content.startswith("Search"):
        
        name = re.sub(r'^([Ss]earch) ', '', message.content)
        print(name)
        movies = search_movie(name)
        print(movies)
        
        if len(movies) > 0:
            await message.channel.send(f"found these movies:\n```\n{search_movie(name)}\n```")

        else:
            await message.channel.send(f"couldn't find any movies for `{name}` :cry:")

    if message.content.startswith('what is this'):

        await message.channel.send('Im Judy bitch and I do everything but for you I will download movies.\n You can say hey bitch download and specify your film of choice and I will do my best to find it. You can roll the dice. You can ask why? in order to get minesweeper, you will lose, Judy always wins minesweeper.Tell me I seem like a bottom and see what happens. Discover something great if you tell me that Im wrong.')         


#@tasks.loop(seconds=10)
#async def check_torrents():
#    print("check torrents")


client.run('OTQ0Nzk5MjE5MDk5NzY2ODc1.YhG21w.XJvkIYEGvxTUPMwgIxZ6icSvZzw')



