import plexapi
from plexapi.server import PlexServer
import datetime

token = open("token").read().strip()
baseurl = 'http://ap6r0.bysh.me:5453'
plex = PlexServer(baseurl, token)


