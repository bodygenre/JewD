from discord.ext import tasks
from modules.asynctools import asyncget
import requests
import xml.etree.ElementTree as ET


torrents = {}


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


@tasks.loop(hours=1)
async def get_new_youtube_movies():
    print("getting new youtube movies")
    
    channels = [ t.strip() for t in open("/home/hd1/tetsuharu/JewD/data/youtube_channel_list.txt").readlines() ]
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





def register(bot):
    # check_torrents.start()
    # check_dead_meat.start()
    # get_new_youtube_movies.start()
    pass


