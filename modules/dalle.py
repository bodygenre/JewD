from discord.ext import tasks
import asyncio
import aiohttp
import base64
from PIL import Image
from io import BytesIO
import random
import datetime



conversation_mode = False
dalle_channel = 989705155446448178




async def gen_images(query):
    data = {"prompt": query}
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.post("https://backend.craiyon.com/generate", json=data) as resp:
            print(f"{query} -- {resp.status}")
            j = await resp.json()
            return [ base64.b64decode(img) for img in j['images'] ]

async def gen_image(query, retries=2):
    if retries < 0:
        print(f"ran out of retries for {query}")
        return None

    try:
        imgs = await gen_images(query)
        dims = (734,734)
        dest = Image.new('RGB', dims)
        img = Image.open(BytesIO(imgs[0]))
        dest.paste(img, (0,0))
    
        r = int(random.random()*1000000000000)
        dest.save(f"tmp_{r}.png")
        with open(f"tmp_{r}.png", "rb") as f:
            d = f.read()
    
        return d
    except Exception as e:
        print(f"exception for {query}", e)
        await asyncio.sleep(30)
        return await gen_image(query, retries=retries-1)
        
        return None



async def gen_image_grid(query, retries=2):
    if retries < 0:
        print(f"ran out of retries for {query}")
        return None

    print(f"gen_image_grid for {query} -- {retries}")

    try:
        imgs = await gen_images(query)
        #imgs = []
        #for i in range(9):
        #    with open(f"millhouse_{i}.png", "rb") as f:
        #        imgs.append(f.read())
        dest = Image.new('RGB', (734*3, 734*3))
        for i in range(9):
            y = i%3
            x = int(i/3)
            img = Image.open(BytesIO(imgs[i]))
            dest.paste(img, (x*734, y*734))
    
        r = int(random.random()*1000000000000)
        dest.save(f"tmp_{r}.png")
        with open(f"tmp_{r}.png", "rb") as f:
            d = f.read()
        #os.remove(f"tmp_{r}.png")
    
        return d
    except Exception as e:
        print(f"exception for {query}", e)
        await asyncio.sleep(30)
        return await gen_image_grid(query, retries=retries-1)
        
        return None

conversation_mode = False


async def on_reaction_add(reaction, user):
    global dalle_channel
    print("on reaction add")
    print(reaction)
    print(reaction.message)
    print(reaction.message.attachments)
    if reaction.message.channel.id != dalle_channel:
        return
    attachments = reaction.message.attachments
    if len(attachments) > 0:
        img = attachments[0]
        print("img",img)
        async with aiohttp.ClientSession() as session:
            async with session.get(str(img)) as resp:
                msg = reaction.message.content
                msg = re.sub(r"^<[^>]+> \"","", re.sub(r"\"$","", msg))
                n = datetime.now()
                datestr = n.strftime("%Y%m%d%H%M")
                with open(f"saved/{datestr} {msg}.png","wb") as f:
                    f.write(await resp.read())


async def on_message(message):
    if message.channel.id == dalle_channel:
        if message.content.startswith('!'):
            return

        if conversation_mode:

            query = message.content.replace("!dalle ","")
            print("making conversational images for " + query)

            user_id = message.author.id
            channel = message.channel

            await message.delete()
            try:
                await message.delete()
                await message.delete()
                await message.delete()
            except:
                pass

            idx = len(dalle_prompts)
            dalle_prompts.append(query)
            dalle_users.append(user_id)

            image = await gen_image_grid(query)

            if image is None:
                print(f"failed to get images for {query}")
                dalle_prompts.remove(idx)
                dalle_users.remove(idx)
                return


            dalle_images[query] = image
            print("saving conversational images for " + query)

            # store images in the order they were provided
            # attempt to clear the queue

            while len(dalle_prompts) > 0:

                if dalle_prompts[0] not in dalle_images:
                    await asyncio.sleep(0.5)
                    continue
                prompt = dalle_prompts.pop(0)
                user = dalle_users.pop(0)
                image = dalle_images[prompt]
                del dalle_images[prompt]
                await channel.send(f"<@{user}> \"{prompt}\"", file=discord.File(BytesIO(image), f"{query}.png"))

        else:

            # TODO: save images that get emoji reacts
            print(message)
            print(message.content)

            query = message.content
            print("making images for " + query)
            image = await gen_image_grid(query)
            await message.channel.send(query, file=discord.File(BytesIO(image), f"{query}.png"))

def register(bot):
    @bot.command(name='!conversation')
    async def conversation(ctx):
        await ctx.send("turning off conversation mode" if conversation_mode else "turning on conversation mode")
        conversation_mode = not conversation_mode

    @bot.command(name='!dallehelp')
    async def dallehelp(ctx):
        await ctx.send(f"How to use our lil' dalle:\n- Say anything into this chat. Judy will get a pic from dalle.\n- say !conversation to turn conversation mode on and off\n- Add a react to a photo to save it at this page http://bodygen.re:8055/")

    @bot.command(name='dalle')
    async def dalle(ctx):
        query = re.sub(r'^[Dd]alle ', '', ctx.message.content)
        print("making images for " + query)
        image = await gen_image_grid(query)
        await ctx.send(query, file=discord.File(BytesIO(image), f"{query}.png"))


    # dalle_the_news.start()





last_news_headlines = set()

@tasks.loop(minutes=5)
async def dalle_the_news():
    global last_news_headline
    print("dalle_the_news")
    xml = requests.get("https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com&hl=en-US&gl=US&ceid=US:en").content
    xml = ET.XML(xml)
    item = xml.find('channel').findall('item')[-1]
    title = item.find('title').text
    if title in last_news_headlines:
        return
    last_news_headlines.add(title)
    url = item.find('link').text
    query = re.sub(r' - The Associated Press.*', '', title)
    print("making images for " + query)
    image = await gen_image_grid(query)
    NEWS_CHANNEL = 989436171333537843
    channel = channel = bot.get_channel(NEWS_CHANNEL)
    print("done making images")
    url = ""
    await channel.send(query+"\n"+url, file=discord.File(BytesIO(image), f"{query}.png"))
