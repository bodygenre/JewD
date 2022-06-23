import asyncio
import aiohttp
import base64
from PIL import Image
from io import BytesIO
import random

async def gen_images(query):
    data = {"prompt": query}
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.post("https://backend.craiyon.com/generate", json=data) as resp:
            j = await resp.json()
            return [ base64.b64decode(img) for img in j['images'] ]

async def gen_image_grid(query):
    imgs = await gen_images(query)
    #imgs = []
    #for i in range(9):
    #    with open(f"millhouse_{i}.png", "rb") as f:
    #        imgs.append(f.read())
    dest = Image.new('RGB', (256*3, 256*3))
    for i in range(9):
        y = i%3
        x = int(i/3)
        img = Image.open(BytesIO(imgs[i]))
        dest.paste(img, (x*256, y*256))

    r = int(random.random()*1000000000000)
    dest.save(f"tmp_{r}.png")
    with open(f"tmp_{r}.png", "rb") as f:
        d = f.read()

    return d

async def main():
    print("hello")
    img = await gen_image_grid("millhouse batallion")
    with open('c.png','wb') as f:
        f.write(img)
    #for i in range(len(imgs)):
    #    print(i)
    #    with open(f"millhouse_{i}.png", "wb") as f:
    #        f.write(imgs[i])
    
    print("done")
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())


