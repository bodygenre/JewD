from discord.ext import tasks
import random
import json

# name: Achilles

with open("data/markov.brain", "r") as f:
  brain = json.load(f)

# LEARN THINGS
def learn_sentence(brain, sentence):
  if "\n" in sentence:
    sentences = sentence.split("\n")
    for s in sentences:
      learn_sentence(brain, s)
    return

  with open("data/learned_sentences.txt","a+") as f:
    f.write(sentence + "\n")

  sentence_words = sentence.split(" ")
  
  for index in range(len(sentence_words)-1):
    word = sentence_words[index]
    next_word = sentence_words[index+1]
  
    if word not in brain:
      brain[word] = []
  
    brain[word].append(next_word)
  
  last_word = sentence_words[-1]
  if last_word not in brain:
    brain[last_word] = []
  brain[last_word].append('.')

  with open("data/markov.brain", "w") as f:
    json.dump(brain, f)

# SAY THINGS
def generate_sentence(brain, starter_word):
  word = starter_word
  
  sentence = ""
  while word != ".":
    sentence = sentence + " " + word
    possible_next_words = brain[word]
    word = random.choice(possible_next_words)
  return sentence




last_news_headlines = set()

@tasks.loop(minutes=5)
async def markov_the_news():
        global last_news_headline
        print("markov_the_news")
        xml = requests.get("https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com&hl=en-US&gl=US&ceid=US:en").content
        xml = ET.XML(xml)
        item = xml.find('channel').findall('item')[-1]
        title = item.find('title').text
        if title in last_news_headlines:
            return
        last_news_headlines.add(title)
        url = item.find('link').text
        query = re.sub(r' - The Associated Press.*', '', title)
        markov.learn_sentence(markov.brain, query)


last_npr_summaries = set()

@tasks.loop(minutes=5)
async def markov_the_npr_news():
        global last_npr_summaries
        print("markov_the_npr_news")
        channels = [ 1019, 1017, 2047 ]
        for chan in channels:
            summaries = news_feeds.get_npr_news(chan)
            for s in summaries:
                markov.learn_sentence(markov.brain, s)




def register(bot):
    # markov_the_news.start()
    # markov_the_npr_news.start()
    pass


