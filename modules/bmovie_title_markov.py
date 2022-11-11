from modules.plexclient import plex
import hashlib
import random
import datetime
import re
import json

rerun = True
#rerun = False

if rerun:
    b = plex.library.section('B Movies')
    
    bmovies = b.search()
    
    brain = { '<start>': [] }
    titles = []
    for m in bmovies:
        d = m.duration / 1000 / 60 # minutes
        t = m.title
        t = t.replace(",", "")
        t = t.replace(".", "")
        t = t.replace(":", "")
        t = t.replace(" - ", "")
        t = re.sub(r"Eng Ita Subs.*", "", t)
        t = re.sub(r"Eng Subs.*", "", t)
        t = t.replace('"', "")
        t = t.lower()
        words = t.split(" ")
        brain['<start>'].append(words[0])
        for a,b in zip(words[0:-1], words[1:]):
            if a not in brain: brain[a] = []
            brain[a].append(b)
        if words[-1] not in brain: brain[words[-1]] = []
        brain[words[-1]].append('.')
        titles.append(words)
    with open('data/bmovie_title.brain','w') as f:
        f.write(json.dumps({ "brain": brain, "titles": titles }))
else:
    with open('data/bmovie_title.brain') as f:
        j = json.loads(f.read())
        brain = j['brain']
        titles = j['titles']

def gen_chain(brain, w):
    chain = []
    while w != '.':
        w = random.choice(brain[w])
        chain.append(w)
    return chain[0:-1]

def gen_title():
    global brain
    c = []
    while (len(c) < 3 or len(c) > 6) and " ".join(c) not in titles:
        c = gen_chain(brain, '<start>')
    c = [ w.capitalize() for w in c ]
    title = " ".join(c)
    fakeyear = int(hashlib.md5(title.encode('utf-8')).hexdigest(), 16) % 10 + 1980
    return title + f" ({fakeyear})"


def register(bot):
    @bot.command("!title")
    async def title(ctx):
        m = 1
        if ctx.message.content.startswith("!title "):
            m = int(ctx.message.content.replace("!title ", ""))
        for i in range(m):
            await ctx.send(gen_title())




