import requests
from pyquery import PyQuery as pq

html = requests.get('https://www.imdb.com/name/nm0000706/?ref_=tt_cl_t_1').content
d = pq(html)
rows = d('#filmography .filmo-category-section:first .filmo-row')
for row in rows:
    name = row.find('b').find('a').text.strip()
    year = row.find('span').text.strip()
    print(name, year)

