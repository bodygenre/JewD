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

if __name__ == '__main__':
    # paredFlight = getMatchedFlights(["SFO","IND"],"20220508","20220511")
    paredFlight = getMatchedFlights(["SFO","IND","MCO"],"20220508","20220511")

    for price,city,airports,urls in paredFlight:
        print(price,city,airports)
        print(urls)
