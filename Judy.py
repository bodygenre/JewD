import os
import random
import glob
from types import ModuleType

from discord.ext import commands
import discord
from datetime import datetime

TOKEN = open('data/discord_token').read().strip()

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

previous_server_restart = datetime.now()


on_message_handlers = []
on_reaction_add_handlers = []


bot.HEYBITCHDOWNLOAD_CHANNEL_ID = 944851560981225512

@bot.event
async def on_ready():
    print( 'We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(msg):
    for handler in on_message_handlers:
        await handler(msg)


@bot.event
async def on_reaction_add(reaction, user):
    for handler in on_reaction_add_handlers:
        await handler(reaction, user)


# import all modules/
for t in glob.glob('modules/*.py'):
   __import__(t.replace('/','.')[0:-3])
modules = __import__('modules')

# register all module endpoints
for k, m in modules.__dict__.items():
    if isinstance(m, ModuleType):
        m.register(bot)
        if 'on_message' in m.__dict__:
            on_message_handlers.append(m.on_message)
        if 'on_reaction_add' in m.__dict__:
            on_reaction_add_handlers.append(m.on_reaction_add)


bot.run(TOKEN)

