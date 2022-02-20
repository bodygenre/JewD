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

    if message.content.startswith('that is mean'):

        await message.channel.send('your emotions amuse me. Im the beez kneez boss sauce')

    if message.content.startswith('thats ridiculous'):
       
        await message.channel.send('Dont pee on my leg and tell me its raining!')

    if message.content.startswith('it is raining'):

        await message.channel.send('im an entertainer and im paid as an entertainer')

    if message.content.startswith('thats cool'):

        await message.channel.send('its nice to leave on top.')
    
    if message.content.startswith('you seem like a bottom'):

        await message.channel.send('Who is interested in that? Who is interested in the warm and fuzzy? There’s enough warm and fuzzy on television')

    if message.content.startswith('i  like warmth'):

        await message.channel.send('I still think an egg Mcmuffin is the best breakfast')

    if message.content.startswith('youre wrong'):

        await message.channel.send('and youre guilty')

    
client.run('OTQ0Nzk5MjE5MDk5NzY2ODc1.YhG21w.XJvkIYEGvxTUPMwgIxZ6icSvZzw')



