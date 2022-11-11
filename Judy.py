import os
import random
import glob
from types import ModuleType

from discord.ext import commands
import discord
from datetime import datetime

TOKEN = "OTQ0Nzk5MjE5MDk5NzY2ODc1.Gru9vD.o5RMpayPhc5jfQIHtSHAd5wjN6kR-FB6-34Dcs"

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

revious_server_restart = datetime.now()

@bot.event
async def on_ready():
    print( 'We have logged in as {0.user}'.format(bot))


@bot.command(name='99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


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




print("bot config", bot.command_prefix)
@bot.command(name='asdf')
async def asdf(msg):
    print("COMMAND: asdf")


bot.run(TOKEN)
