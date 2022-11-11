import requests
import itertools

def flights(airport,departDate,returnDate):
    url = 'https://www.kayak.com/s/horizon/exploreapi/destinations?airport='+airport+'&budget=&depart='+departDate+'&return='+returnDate+'&duration=&exactDates=true&flightMaxStops0=&stopsFilterActive=false&topRightLat=0&topRightLon=0&bottomLeftLat=0&bottomLeftLon=0&zoomLevel=5&selectedMarker=&themeCode=&selectedDestination='
    response = requests.get(url)
    jsonresponse = response.json()
    destinations = jsonresponse['destinations']
    flights1 = []
    for record in destinations:
        flightURL = "https://www.kayak.com"+record['clickoutUrl']
        flightInfo = record['flightInfo']
        endPoint = record['airport']
        city = record['city']
        cityName = city['name']
        if flightInfo['priceUSD'] < 500:
            flights1.append([flightInfo['priceUSD'],endPoint['shortName'],cityName,flightURL])
    print(len(flights1))
    return flights1

def getMatchedFlights(airports,departDate,returnDate):
    print("doing getmatchedflights")
    print(airports)
    print(departDate)
    print(returnDate)
    flightses = []
    for airport in airports:
        flightses.append(flights(airport,departDate,returnDate))

    matchedFlight = []

    for flightgroup in itertools.product(*flightses):
        cities = [ f[2] for f in flightgroup ]
        if cities.count(cities[0]) != len(cities):
            continue

        pricetotal = 0
        airports = []
        urls = []
        for f in flightgroup:
            pricetotal += f[0]
            airports.append(f[1])
            urls.append(f[3])
        if pricetotal / len(airports) < 800:
            matchedFlight.append([pricetotal, cities[0], airports, urls])


    matchedFlight = sorted(matchedFlight, key=lambda x: x[0])

    paredFlight = []
    seen = set()
    for price,city,airports,urls in matchedFlight:
        if city not in seen:
            seen.add(city)
            paredFlight.append([price,city,airports,urls])

    paredFlight = reversed(paredFlight)

    return paredFlight



async def on_message(message):
    if message.content.startswith('meet me ') or message.content.startswith('Meet me '):
        #await message.add_reaction(':mag_right:')
        s = message.content[8:]
        parts = s.split(" ")
        end = parts.pop()
        start = parts.pop()
        airports = [ p.upper() for p in parts ]
        flights = list(getMatchedFlights(airports, start, end))
        res = []
        for price, city, airports, urls in flights[-5:]:
            p = f"${math.floor(price)}"
            pp = f"${math.floor(price/len(airports))}/per"
            u = "\n".join([ '<'+t+'>' for t in urls ])
            a = ", ".join(airports)
            res.append(p + "\t" + pp + "\t" + city + "\t" + a + "\n" + u)
        await message.channel.send("\n".join(res))

    if message.content.startswith('new'):
        await dalle_the_news()
        #xml = requests.get("https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com&hl=en-US&gl=US&ceid=US:en").content
        #xml = ET.XML(xml)
        #title = xml.find('channel').findall('item')[-1].find('title').text
        #query = re.sub(r' - The Associated Press.*', '', title)
        #print("making images for " + query)
        #image = await gen_image_grid(query)
        #await message.channel.send(query, file=discord.File(BytesIO(image), f"{query}.png"))


def register(bot):
    pass



