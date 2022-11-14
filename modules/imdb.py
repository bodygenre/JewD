#from imdb import IMDb

#ia = IMDb()

def search_movie(movie):
    movies = ia.search_movie(movie)[0:10]
    return "\n".join([ f"{m.get('title')} ({m.get('year')})" for m in movies ])


async def on_message(message):
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

def register(bot):
    pass
