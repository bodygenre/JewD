import re
from datetime import datetime
from modules.asynctools import asyncget
from modules.downloaders import getbest

previous_server_restart = datetime.now()


def kill_backend():
    global previous_server_restart
    n = datetime.now()
    if n - previous_server_restart > timedelta(0,10,0):
        os.system("/home/hd1/tetsuharu/bin/killbackend.sh")
        previous_server_restart = n


def register(bot):
    pass


async def on_message(message):

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

    if message.content.startswith('free space') or message.content.startswith('Free space'):
        p = subprocess.Popen(["df"], stdout=subprocess.PIPE)
        out,err = p.communicate()
        parts = re.split(r" +", next(t for t in out.decode('utf-8').split("\n") if 'md125' in t))
        free = int(parts[3])/1024/1024
        num_movies = int(free/5)
        pctfree = 100-int(float(parts[4].replace('%','')))

        await message.channel.send(f"free space on disk: {pctfree}%, that's about {num_movies} movies")


    if message.content.startswith("fix backend"):
        kill_backend()
