import requests

def get_npr_news(num):
    j = requests.get(f"https://feeds.npr.org/{num}/feed.json").json()
    return [ t['summary'] for t in j['items'] ]

