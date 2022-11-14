from discord.ext import tasks


bot = None
new_movies_added = []


@tasks.loop(hours=24)
async def notify_new_movies():
    global new_movies_added, bot

    await asyncio.sleep(5)
    channel = bot.get_channel(bot.HEYBITCHDOWNLOAD_CHANNEL_ID)

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


def register(bott):
    global bot
    bot = bott
    #notify_new_movies.start()


