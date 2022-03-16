from imdb import IMDb

ia = IMDb()

def search_movie(movie):
    movies = ia.search_movie(movie)[0:10]
    return "\n".join([ f"{m.get('title')} ({m.get('year')})" for m in movies ])


