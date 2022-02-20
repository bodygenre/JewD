import discord

client = discord.Client()

@client.event
async def on_ready():
    print( 'We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):

        await message.channel.send('Hello!')

    if message.content.startswith('how are you'):

        await message.channel.send('Not as good as your prison sentence.')

client.run('OTQ0Nzk5MjE5MDk5NzY2ODc1.YhG21w.XJvkIYEGvxTUPMwgIxZ6icSvZzw')



