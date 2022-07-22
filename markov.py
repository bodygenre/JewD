import random
import json

# name: Achilles

with open("markov.brain", "r") as f:
  brain = json.load(f)

# LEARN THINGS
def learn_sentence(brain, sentence):
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

  with open("markov.brain", "w") as f:
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

