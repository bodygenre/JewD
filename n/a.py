import re

a = [ k.strip() for k in open('a').readlines() ]

lines = []
curr = ""
for i in a:
  if i[0:5].lower() in [ 'lemoi', 'lamda', 'colla' ]:
    print(curr)
    curr = i
  else:
    curr += " " + i

