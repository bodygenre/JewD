from modules.discordsweeper import makeDiscordMinesweeper

async def on_message(msg):

    if msg.content.startswith('hello'):
        await msg.channel.send('Hello!')

    if msg.content.startswith('how are you'):
        await msg.channel.send('Not as good as your prison sentence.')

    if msg.content.startswith('that is mean'):
        await msg.channel.send('your emotions amuse me. Im the beez kneez boss sauce')

    if msg.content.startswith('thats ridiculous'):
        await msg.channel.send('Dont pee on my leg and tell me its raining!')

    if msg.content.startswith('it is raining'):
        await msg.channel.send('im an entertainer and im paid as an entertainer')

    if msg.content.startswith('thats cool'):
        await msg.channel.send('its nice to leave on top.')

    if msg.content.startswith('you seem like a bottom'):
        await msg.channel.send('Who is interested in that? Who is interested in the warm and fuzzy? There’s enough warm and fuzzy on television')

    if msg.content.startswith('i like warmth'):
        await msg.channel.send('I still think an egg Mcmuffin is the best breakfast')

    if msg.content.startswith('youre wrong'):
        await msg.channel.send('and youre guilty')

    if msg.content.startswith('why?'):
        blah = makeDiscordMinesweeper(7,7,7)

        await msg.channel.send(blah)

    if msg.content.startswith('roll the dice'):

        die_roll = rollDie()

        await msg.channel.send(die_roll)

    if msg.content.startswith('what is this'):

        await msg.channel.send('Im Judy bitch and I do everything but for you I will download movies.\n You can say hey bitch download and specify your film of choice and I will do my best to find it. You can roll the dice. You can ask why? in order to get minesweeper, you will lose, Judy always wins minesweeper.Tell me I seem like a bottom and see what happens. Discover something great if you tell me that Im wrong.')

def register(bot):
    pass



