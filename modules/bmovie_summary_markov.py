from modules.plexclient import plex
import discord
import hashlib
import random
import datetime
import re
import json

from modules import bmovie_title_markov
from modules.dalle import gen_image
from io import BytesIO

rerun = True
#rerun = False

if rerun:
    b = plex.library.section('B Movies')
    
    bmovies = b.search()
    
    brain = { '<start>': [] }
    summaries = []
    i=0
    for m in bmovies:
        d = m.duration / 1000 / 60 # minutes
        t = m.summary
        #t = t.replace(",", "")
        #t = t.replace(".", "")
        #t = t.replace(":", "")
        #t = t.replace(" - ", "")
        #t = re.sub(r"Eng Ita Subs.*", "", t)
        #t = re.sub(r"Eng Subs.*", "", t)
        t = t.replace('"', "")
        t = t.replace("\n", " ")
        t = t.lower()
        words = t.split(" ")
        brain['<start>'].append(words[0])
        for a,b in zip(words[0:-1], words[1:]):
            if a not in brain: brain[a] = []
            brain[a].append(b)
        if words[-1] not in brain: brain[words[-1]] = []
        brain[words[-1]].append('.')
        summaries.append(words)
    with open('data/bmovie_summary.brain','w') as f:
        f.write(json.dumps({ "brain": brain, "summaries": summaries }))
else:
    with open('data/bmovie_summary.brain') as f:
        j = json.loads(f.read())
        brain = j['brain']
        summaries = j['summaries']

def gen_chain(brain, w):
    chain = []
    while w != '.':
        w = random.choice(brain[w])
        chain.append(w)
    return chain[0:-1]

def gen_summary():
    global brain
    summary = []
    for i in range(random.randint(1,3)):
        c = []
        while len(c) < 5 or len(c) > 15:
            c = gen_chain(brain, '<start>')
        summary.append(" ".join(c).capitalize())
    return " ".join(summary)



def register(bot):
    @bot.command(name='!summary')
    async def summary(ctx):
        t = bmovie_title_markov.gen_title()
        s = gen_summary()

        query = re.sub(r' \([0-9]+\)$', '', t + " " + s)
        print("making images for fake movie: " + query)
        image = await gen_image(query)
        await ctx.send(f"{t}\n> {s}\n", file=discord.File(BytesIO(image), f"{query}.png"))


