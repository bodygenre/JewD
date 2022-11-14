import requests
import asyncio

def asyncget(url):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: requests.get(url, verify=False, timeout=60*5).json())


def register(bot):
    pass
