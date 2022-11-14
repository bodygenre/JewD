import requests
import re
import subprocess
from modules.asynctools import asyncget


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


async def on_message(message):
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


def register(bot):
    pass


