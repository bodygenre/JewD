import requests
from modules import markov

achilles_channel = 999885857685250118

async def tts(user, text):
  global voice
  if voice is None: return
  tries = 5
  done = False
  while not done and tries > 0:
    try:
      print("tryna make an mp3", text)
      res = requests.post("https://ttsmp3.com/makemp3_new.php", data={"msg": text, "lang": "Justin", "source": "ttsmp3member", "user": 213928}, timeout=2)
      #res = requests.post("https://ttsmp3.com/makemp3_new.php", data={"msg": text, "lang": "Justin", "source": "ttsmp3"}, timeout=2)
      j = res.json()
      print(j)
      res = requests.get(j['URL'], timeout=2)
      with open(j['MP3'], 'wb') as f:
        f.write(res.content)
      print("wrote audio file")
      done = True
    except Exception as e:
      print(e)
      tries -= 1
      await asyncio.sleep(1)
  if tries <= 0: return
  audio = FFmpegPCMAudio(j['MP3'])
  tries = 10
  while True:
    try:
      voice.play(audio)
      return
    except:
      if tries <= 0: return
      tries -= 1
      await asyncio.sleep(1)



async def on_message(message):
    # learn everything
    msgs = message.content.split("\n")
    for msg in msgs:
        mmsgs = msg.split(". ")
        for mmsg in mmsgs:
            markov.learn_sentence(markov.brain, mmsg)


    if message.content.startswith("!vc"):
      global voice
      user = message.author
      if user.voice is None:
        return
      c = user.voice.channel
      if not voice:
        voice = await c.connect()
      else:
        voice.move_to(c)

    if message.content.startswith("!novc"):
      await voice.disconnect()
      voice = None

    if message.content.startswith("achilles: ") or message.content.startswith("Achilles: ") or message.content.startswith("A: ") or message.content.startswith("a: "):
        if message.content.startswith("A: ") or message.content.startswith("a: "):
          msg = message.content[3:]
        else:
          msg = message.content[10:]
        markov.learn_sentence(markov.brain, msg)
        word = random.choice(msg.split(" "))
        new_sentence = markov.generate_sentence(markov.brain, word)
        markov.learn_sentence(markov.brain, new_sentence)
        sleeptime = len(new_sentence)/20.0
        await asyncio.sleep(sleeptime)
        await message.channel.send("(Achilles) " + new_sentence)

    elif message.channel.id == achilles_channel:
        msg = message.content
        markov.learn_sentence(markov.brain, msg)
        word = random.choice(msg.split(" "))
        new_sentence = markov.generate_sentence(markov.brain, word)
        markov.learn_sentence(markov.brain, new_sentence)
        sleeptime = len(new_sentence)/20.0
        await asyncio.sleep(sleeptime)
        await tts(message.author, new_sentence)
        await message.channel.send(new_sentence)


    elif 'achilles' in message.content or 'Achilles' in message.content:
        msg = message.content
        markov.learn_sentence(markov.brain, msg)
        word = random.choice(msg.split(" "))
        new_sentence = markov.generate_sentence(markov.brain, word)
        markov.learn_sentence(markov.brain, new_sentence)
        sleeptime = len(new_sentence)/20.0
        await asyncio.sleep(sleeptime)
        await message.channel.send("(Achilles) " + new_sentence)


def register(bot):
    pass


