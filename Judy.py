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


def asyncget(url):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: requests.get(url, verify=False, timeout=60*5).json())


intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
intents.message_content = True

new_movies_added = []

bot = commands.Bot(command_prefix='~', help_command=None, intents=intents)

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

    if message.content.startswith("!title"):
        m = 1
        if message.content.startswith("!title "):
            m = int(message.content.replace("!title ", ""))
        for i in range(m):
            await message.channel.send(bmovie_title_markov.gen_title())        

    if message.content.startswith("!markovmovie"):
        t = bmovie_title_markov.gen_title()
        s = bmovie_summary_markov.gen_summary()
        
        query = re.sub(r' \([0-9]+\)$', '', t + " " + s)
        print("making images for fake movie: " + query)
        image = await gen_image(query)
        await message.channel.send(f"{t}\n> {s}\n", file=discord.File(BytesIO(image), f"{query}.png"))
        

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

    achilles_channel = 999885857685250118
    #achilles_channel = 788925423420964912

    # learn everything
    msgs = message.content.split("\n")
    for msg in msgs:
        mmsgs = msg.split(". ")
        for mmsg in mmsgs:
            markov.learn_sentence(markov.brain, mmsg)


    if message.content.startswith("!vc"):
      global voice
      user = message.author
      if user.voice is None:
        return
      c = user.voice.channel
      if not voice:
        voice = await c.connect()
      else:
        voice.move_to(c)
      
    if message.content.startswith("!novc"):
      await voice.disconnect()
      voice = None

    async def tts(user, text):
      global voice
      if voice is None: return
      tries = 5
      done = False
      while not done and tries > 0:
        try:
          print("tryna make an mp3", text)
          res = requests.post("https://ttsmp3.com/makemp3_new.php", data={"msg": text, "lang": "Justin", "source": "ttsmp3member", "user": 213928}, timeout=2)
          #res = requests.post("https://ttsmp3.com/makemp3_new.php", data={"msg": text, "lang": "Justin", "source": "ttsmp3"}, timeout=2)
          j = res.json()
          print(j)
          res = requests.get(j['URL'], timeout=2)
          with open(j['MP3'], 'wb') as f:
            f.write(res.content)
          print("wrote audio file")
          done = True
        except Exception as e:
          print(e)
          tries -= 1
          await asyncio.sleep(1)
      if tries <= 0: return
      audio = FFmpegPCMAudio(j['MP3'])
      tries = 10
      while True:
        try:
          voice.play(audio)
          return
        except:
          if tries <= 0: return
          tries -= 1
          await asyncio.sleep(1)



    if message.content.startswith("achilles: ") or message.content.startswith("Achilles: ") or message.content.startswith("A: ") or message.content.startswith("a: "):
        if message.content.startswith("A: ") or message.content.startswith("a: "):
          msg = message.content[3:]
        else:
          msg = message.content[10:]
        markov.learn_sentence(markov.brain, msg)
        word = random.choice(msg.split(" "))
        new_sentence = markov.generate_sentence(markov.brain, word)
        markov.learn_sentence(markov.brain, new_sentence)
        sleeptime = len(new_sentence)/20.0
        await asyncio.sleep(sleeptime)
        await message.channel.send("(Achilles) " + new_sentence)

    elif message.channel.id == achilles_channel:
        msg = message.content
        markov.learn_sentence(markov.brain, msg)
        word = random.choice(msg.split(" "))
        new_sentence = markov.generate_sentence(markov.brain, word)
        markov.learn_sentence(markov.brain, new_sentence)
        sleeptime = len(new_sentence)/20.0
        await asyncio.sleep(sleeptime)
        await tts(message.author, new_sentence)
        await message.channel.send(new_sentence)


    elif 'achilles' in message.content or 'Achilles' in message.content:
        msg = message.content
        markov.learn_sentence(markov.brain, msg)
        word = random.choice(msg.split(" "))
        new_sentence = markov.generate_sentence(markov.brain, word)
        markov.learn_sentence(markov.brain, new_sentence)
        sleeptime = len(new_sentence)/20.0
        await asyncio.sleep(sleeptime)
        await message.channel.send("(Achilles) " + new_sentence)


    if message.content.startswith('free space') or message.content.startswith('Free space'):
        p = subprocess.Popen(["df"], stdout=subprocess.PIPE)
        out,err = p.communicate()
        parts = re.split(r" +", next(t for t in out.decode('utf-8').split("\n") if 'md125' in t))
        free = int(parts[3])/1024/1024
        num_movies = int(free/5)
        pctfree = 100-int(float(parts[4].replace('%','')))
        
        await message.channel.send(f"free space on disk: {pctfree}%, that's about {num_movies} movies")


    if message.content.startswith('roll the dice'):

        die_roll = rollDie()

        await message.channel.send(die_roll)

    if message.content.startswith('dalle ') or message.content.startswith('Dalle'):

        query = re.sub(r'^[Dd]alle ', '', message.content)
        print("making images for " + query)
        image = await gen_image_grid(query)
        await message.channel.send(query, file=discord.File(BytesIO(image), f"{query}.png"))


    if message.content.startswith('!conversation'):
        await message.channel.send("turning off conversation mode" if conversation_mode else "turning on conversation mode")
        conversation_mode = not conversation_mode

    if message.content.startswith('!dallehelp'):
        await message.channel.send(f"How to use our lil' dalle:\n- Say anything into this chat. Judy will get a pic from dalle.\n- say !conversation to turn conversation mode on and off\n- Add a react to a photo to save it at this page http://bodygen.re/")

    if message.channel.id == dalle_channel:
        if message.content.startswith('!'):
            return

        if conversation_mode:
    
            query = message.content.replace("!dalle ","")
            print("making conversational images for " + query)

            user_id = message.author.id
            channel = message.channel
    
            await message.delete()
            try:
                await message.delete()
                await message.delete()
                await message.delete()
            except:
                pass    

            idx = len(dalle_prompts)
            dalle_prompts.append(query)
            dalle_users.append(user_id)

            image = await gen_image_grid(query)

            if image is None:
                print(f"failed to get images for {query}")
                dalle_prompts.remove(idx)
                dalle_users.remove(idx)
                return
    
    
            dalle_images[query] = image
            print("saving conversational images for " + query)
            
            # store images in the order they were provided
            # attempt to clear the queue
            
            while len(dalle_prompts) > 0:
                
                if dalle_prompts[0] not in dalle_images:
                    await asyncio.sleep(0.5)
                    continue
                prompt = dalle_prompts.pop(0)
                user = dalle_users.pop(0)
                image = dalle_images[prompt]
                del dalle_images[prompt]
                await channel.send(f"<@{user}> \"{prompt}\"", file=discord.File(BytesIO(image), f"{query}.png"))

        else: 
    
            # TODO: save images that get emoji reacts
            print(message)
            print(message.content)
    
            query = message.content
            print("making images for " + query)
            image = await gen_image_grid(query)
            await message.channel.send(query, file=discord.File(BytesIO(image), f"{query}.png"))
        
        

    if message.content.lower().startswith("youtube "):
        url = message.content[8:]
        print('youdowning ', url)
        subprocess.Popen(["/home/hd1/tetsuharu/bin/youdown", url], stdout=subprocess.PIPE)

    if message.content.lower().startswith("youtube\n"):
        urls = message.content.split("\n")[1:]
        for url in urls:
            print('youdowning ', url)
            subprocess.Popen(["/home/hd1/tetsuharu/bin/youdown", url], stdout=subprocess.PIPE)

    if message.content.startswith('hey bitch download! ') or message.content.startswith('Hey bitch download!') or message.content.startswith('download! ') or message.content.startswith('Download! ') or message.content.startswith('download!'):

        if "\n" in message.content:
            names = message.content.split("\n")[1:]
            print("downloading bulk: ", "::".join(names))
            await message.add_reaction('👀')
            for name in names:
                getbest(name, message.channel)
        else:
            name = re.sub(r'^([Hh]ey bitch download|[Dd]ownload)! ', '', message.content)
            await getbest(name, message.channel, message=message)

    if message.content.startswith("fix backend"):
        kill_backend()

    if message.content.startswith("all movies for actor") or message.content.startswith("All movies for actor"):
        name = re.sub(r'^[Aa]ll movies for actor ', '', message.content)
        if "bowie" in name.lower(): return
        ia = IMDb()
        person = ia.search_person(name)[0]
        html = requests.get('https://www.imdb.com/name/nm' + str(person.personID) + '/?ref_=tt_cl_t_1').content
        d = pq(html)
        rows = d('#filmography .filmo-category-section:first .filmo-row')
        movies = list()
        for row in rows:
            name = row.find('b').find('a').text.strip()
            year = row.find('span').text.strip()
            movies.append(f"{name} {year}")
        movies = list(set(movies))

        await message.add_reaction('👀')
        for movie in movies:
            if "TV Series" in movie:
                continue
            await getbest(movie, message.channel, showmissing=True, message=message)

    if message.content.startswith("search") or message.content.startswith("Search"):
        
        name = re.sub(r'^([Ss]earch) ', '', message.content)
        print(name)
        movies = search_movie(name)
        print(movies)
        
        if len(movies) > 0:
            await message.channel.send(f"found these movies:\n```\n{search_movie(name)}\n```")

        else:
            print('sending react emoji')
            await message.react('\N{NO ENTRY SIGN}')
#            await message.channel.send(f"couldn't find any movies for `{name}` :cry:")

    if message.content.startswith('what is this'):

        await message.channel.send('Im Judy bitch and I do everything but for you I will download movies.\n You can say hey bitch download and specify your film of choice and I will do my best to find it. You can roll the dice. You can ask why? in order to get minesweeper, you will lose, Judy always wins minesweeper.Tell me I seem like a bottom and see what happens. Discover something great if you tell me that Im wrong.')         

    if message.content.startswith('status') or message.content.startswith('Status') or message.content.startswith("Status") or message.content.startswith("status"):
        if message.content in [ "Status", "status" ]:
            m = ' '
        elif message.content[7:10] == "for":
            m = message.content[11:]
        else:
            m = message.content[7:]
        search = re.sub(r"^[Ss]tatus ", "", m)
        search = re.sub(r" +", ".+", search)
        try:
            curr_list = await asyncget("https://bodygen.re:8081/get_active_torrents")
        except:
            kill_backend()
            time.sleep(5)
            try:
                curr_list = await asyncget("https://bodygen.re:8081/get_active_torrents")
            except:
                await message.channel.send("can't tell you about torrents, the backend is down <@800126234297630740>")
        
        if curr_list:
            # restrict list to ones with the search term in it
            match_list = [ t for t in curr_list if re.match(".*" + search + ".*", t['name'], flags=re.IGNORECASE) and t['state'] != 'Seeding' ]
            matches = []
            for m in match_list:
                eta = int(m['eta']/6)/10
                prog = int(m['progress'])
                rate = int(int(m['download_payload_rate'])/1024)
                name = m['name']
                matches.append("{: >10}min {: >4}% {: >6} kbps {}".format(eta, prog, rate, name))
            if len(matches) == 0:
                await message.channel.send(f"Couldn't find any active torrents for `{search}`")
            else:
                await message.channel.send(f"Status for `{search}`:\n```\n" + "\n".join(matches)[:900] + "\n```") 

    if message.content.startswith('make link for') or message.content.startswith('Make link for'):
        search = re.sub(r"^[Mm]ake link for ","",message.content)
        print("https://bodygen.re:8081/search_existing/" + search)
        existing = await asyncget("https://bodygen.re:8081/search_existing/" + search)
        print('existing: ', existing)
        existing = existing['matches']

        # remove subtitle files
        existing = [ t for t in existing if '.srt' not in t and '.ssa' not in t ]
        if len(existing) > 1:
            m = '\n'.join(existing)
            await message.channel.send("Several files match your search:\n```\n" + m[0:1000] + "\n```\n")
        elif len(existing) == 0:
            await message.channel.send(f"Couldnt make link for {search}, didnt find anything")
        else:
            # we have only 1 file we might use
            link = await asyncget(f"https://bodygen.re:8081/make_download_link?path={existing[0]}")
            await message.channel.send(f"{search}: http://tetsuharu.ap6r0.bysh.me/filebrowser/share/{link['hash']}")



    if message.content.startswith('do we have') or message.content.startswith('Do we have') or message.content.startswith('download ') or message.content.startswith('Download '):
        search = re.sub(r"^([Dd]o we have|[Dd]ownload) ","",message.content)
        print("https://bodygen.re:8081/search_existing/" + search)
        existing = await asyncget("https://bodygen.re:8081/search_existing/" + search)
        print('existing: ', existing)
        existing = existing['matches']

        # remove subtitle files
        existing = [ t for t in existing if '.srt' not in t and '.ssa' not in t ]
        if len(existing) > 0:
            m = '\n'.join(existing)
            await message.channel.send("got it already\n```\n" + m[2:1000] + "\n```(if it's not in here, use `download! <moviename>`)")
        elif len(existing) == 0:
            await getbest(search, message.channel, message=message)

 


    if message.content.startswith('meet me ') or message.content.startswith('Meet me '):
        #await message.add_reaction(':mag_right:')
        s = message.content[8:]
        parts = s.split(" ")
        end = parts.pop()
        start = parts.pop()
        airports = [ p.upper() for p in parts ]
        flights = list(getMatchedFlights(airports, start, end))
        res = []
        for price, city, airports, urls in flights[-5:]:
            p = f"${math.floor(price)}" 
            pp = f"${math.floor(price/len(airports))}/per" 
            u = "\n".join([ '<'+t+'>' for t in urls ])
            a = ", ".join(airports)
            res.append(p + "\t" + pp + "\t" + city + "\t" + a + "\n" + u)
        await message.channel.send("\n".join(res))

    if message.content.startswith('new'):
        await dalle_the_news()
        #xml = requests.get("https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com&hl=en-US&gl=US&ceid=US:en").content
        #xml = ET.XML(xml)
        #title = xml.find('channel').findall('item')[-1].find('title').text
        #query = re.sub(r' - The Associated Press.*', '', title)
        #print("making images for " + query)
        #image = await gen_image_grid(query)
        #await message.channel.send(query, file=discord.File(BytesIO(image), f"{query}.png"))
        

async def getbest(name, channel, showmissing=True, message=None):
        try:
            print("https://bodygen.re:8081/getbest/"+name)
            j = await asyncget("https://bodygen.re:8081/getbest/" + name)
        except:
            kill_backend()
            time.sleep(5)
            try:
                print("https://bodygen.re:8081/getbest/"+name)
                j = await asyncget("https://bodygen.re:8081/getbest/" + name)
            except:
                await channel.send("I think the backend is down? <@800126234297630740>")
                return

        if not j['success']:
            print(f"couldnt download `{name}`")
            if showmissing:
                if message:
                    await message.add_reaction('\N{NO ENTRY SIGN}')
                else:
                    await channel.send(f"couldn't find anything for `{name}`")
        else:
            if message:
                await message.add_reaction('\N{SPARKLES}')
            await channel.send(f"downloading: `{j['torrent_name']}`")



#    elif 
        

def kill_backend():
    global previous_server_restart
    n = datetime.now()
    if n - previous_server_restart > timedelta(0,10,0):
        os.system("/home/hd1/tetsuharu/bin/killbackend.sh")
        previous_server_restart = n

    

HEYBITCHDOWNLOAD_CHANNEL_ID = 944851560981225512

@tasks.loop(hours=24)
async def notify_new_movies():
    global new_movies_added

    await asyncio.sleep(5)
    channel = bot.get_channel(HEYBITCHDOWNLOAD_CHANNEL_ID)

    search = ".+"
    curr_list = await asyncget("https://bodygen.re:8081/get_active_torrents")
    
    if curr_list:
        # restrict list to ones with the search term in it
        match_list = [ t for t in curr_list if re.match(".*" + search + ".*", t['name'], flags=re.IGNORECASE) and t['state'] != 'Seeding' ]
        matches = []
        for m in match_list:
            eta = int(m['eta']/6)/10
            prog = int(m['progress'])
            rate = int(int(m['download_payload_rate'])/1024)
            name = m['name']
            matches.append("{: >10}min {: >4}% {: >6} kbps {}".format(eta, prog, rate, name))
            
    if len(new_movies_added) == 0:
        new_movies_added.append("(none)")

    if len(matches) == 0:
        matches.append("(none)")

    await channel.send("New movies added yesterday: \n```\n" + "\n".join(new_movies_added) + "\n```\n" + "Current torrent status: \n```\n" + "\n".join(matches)[:900] + "\n```")
    new_movies_added = []

torrents = {}
shown_torrents = set()
@tasks.loop(seconds=30)
async def check_torrents():
    global torrents

    print("check torrents")
    channel = bot.get_channel(HEYBITCHDOWNLOAD_CHANNEL_ID)
    if channel is None:
        return

    try:
        curr_list = await asyncget("https://bodygen.re:8081/get_active_torrents")
    except:
        kill_backend()
        time.sleep(5)
        try:
            curr_list = await asyncget("https://bodygen.re:8081/get_active_torrents")
        except:
            await channel.send("can't tell you about torrents, the backend is down <@800126234297630740>")
            return

    curr = {}
    for c in curr_list:
        curr[c['hash']] = c

    message = []

    if len(torrents.keys()) > 0:

        for h in torrents.keys():
            if torrents[h]['state'] == 'Seeding':
                continue

            if h not in curr:
#                message.append(f"torrent disappeard? `{torrents[h]['name']}`")
                continue

            old = torrents[h]
            new = curr[h]
            
            if old['state'] == "Downloading" and new['state'] == 'Seeding':
                # TODO
                new_movies_added.append(old['name'])
                message.append(f"torrent complete - `{old['name']}`")
            
            if new['state'] != 'Seeding':
                # if the progress is past 10%, it's probably okay to use the ETA
                if h not in shown_torrents and new['progress'] > 5:
                    shown_torrents.add(h)
                    mins = new['eta'] / 60
                    print("mins: ", mins)
                    if mins < 60:
                        eta = f"{int(mins*10)/10} min"
                    elif mins < 60*24:
                        eta = f"{int(mins/60*10)/10} hr"
                    else:
                        eta = f"{int(mins/60/24*10)/10} days"
                    kbps = new['download_payload_rate'] / 1024
                    print("kbps: ", kbps)
                    if kbps < 1024:
                        speed = f"{int(kbps*10)/10} kbps"
                    else:
                        speed = f"{int(kbps/1024*10)/10} mbps"
                    #message.append(f"{eta}, {speed} - `{new['name']}`")
                    message.append(f"{eta} - `{new['name']}`")
        
        if len(message) > 0:
            await channel.send("\n".join(message))
    else:
        for c in curr_list:
            shown_torrents.add(c['hash'])
    
    torrents = curr


dead_meat_titles = list()
@tasks.loop(minutes=60)
async def check_dead_meat():
    print('check_dead_meat')
     
    try:
        d = requests.get("http://feeds.megaphone.fm/deadmeat", timeout=10).content
    except:
        print("ERROR: check_dead_meat timeout on megaphone url")
        return
    x = ET.XML(d)

    titles = list()
    for item in x.find('channel').findall('item'):
        title = item.find('title').text
        title = re.sub(r'^[^-:]+[-:] ', '', title)
        title = re.sub(r'[\( ][pP]art.*', '', title)
        titles.append(title)

    if len(dead_meat_titles) != 0:
        for title in titles:
            if title not in dead_meat_titles[-5:]:
                try:
                    j = await asyncget("https://bodygen.re:8081/getbest/" + title)
                except:
                    kill_backend()
                    time.sleep(5)
                    try:
                        j = await asyncget("https://bodygen.re:8081/getbest/" + title)
                    except:
                        print(f"ERROR: check_dead_meat, backend timedout for {title}") 
                print('downloading', j)
                dead_meat_titles.append(title)

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

@tasks.loop(hours=1)
async def get_new_youtube_movies():
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
    




last_news_headlines = set()

@tasks.loop(minutes=5)
async def dalle_the_news():
        global last_news_headline
        print("dalle_the_news")
        xml = requests.get("https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com&hl=en-US&gl=US&ceid=US:en").content
        xml = ET.XML(xml)
        item = xml.find('channel').findall('item')[-1]
        title = item.find('title').text
        if title in last_news_headlines:
            return
        last_news_headlines.add(title)
        url = item.find('link').text
        query = re.sub(r' - The Associated Press.*', '', title)
        print("making images for " + query)
        image = await gen_image_grid(query)
        NEWS_CHANNEL = 989436171333537843
        channel = channel = bot.get_channel(NEWS_CHANNEL)
        print("done making images")
        url = ""
        await channel.send(query+"\n"+url, file=discord.File(BytesIO(image), f"{query}.png"))
        

@tasks.loop(minutes=5)
async def markov_the_news():
        global last_news_headline
        print("markov_the_news")
        xml = requests.get("https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com&hl=en-US&gl=US&ceid=US:en").content
        xml = ET.XML(xml)
        item = xml.find('channel').findall('item')[-1]
        title = item.find('title').text
        if title in last_news_headlines:
            return
        last_news_headlines.add(title)
        url = item.find('link').text
        query = re.sub(r' - The Associated Press.*', '', title)
        markov.learn_sentence(markov.brain, query)
        

last_npr_summaries = set()

@tasks.loop(minutes=5)
async def markov_the_npr_news():
        global last_npr_summaries
        print("markov_the_npr_news")
        channels = [ 1019, 1017, 2047 ]
        for chan in channels:
            summaries = news_feeds.get_npr_news(chan)
            for s in summaries:
                markov.learn_sentence(markov.brain, s)
        









#  check_torrents.start()
#check_dead_meat.start()
#check_current_movie.start()
#get_new_youtube_movies.start()
#   change_stream_bot_name.start()
#dalle_the_news.start()
#markov_the_news.start()
#markov_the_npr_news.start()
#    notify_new_movies.start()

bot.run(open("bot_token").read().strip())



