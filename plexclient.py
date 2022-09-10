import plexapi
from plexapi.server import PlexServer
import datetime

token = open("plex_token").read().strip()
baseurl = open("plex_url").read().strip()
plex = PlexServer(baseurl, token)


