import requests
import os
import operator
import datetime
import time

#os.system("clear")

def dtrack(ans, mykey):
    nameans = ans
    APIKEY = mykey
    matchCount = 4

    #Gets PUUID from Summoner Name
    sumByName = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ans.replace(' ','%20')}?api_key={APIKEY}")
    myID = sumByName.json()

    matches = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{myID['puuid']}/ids?queue=420&start=0&count={matchCount}&api_key={APIKEY}")

    # Gets return as a json/list, Splits it into list of dictionaries
    sepList = str(matches.json()).split(",")

    matchList = []      # Appends to a new list with proper formatting
    for i in sepList:   # Cuts random useless characters in match list
        matchList.append(i.replace(" ","").replace("'", "").replace("[", "").replace("]", ""))
    matchData = []

    for i in matchList:
        print(i)
        matchData.append(requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{i}?api_key={APIKEY}").json())

    times = []
    diffs = []

    for i in matchData:
        gameDate = i['info']['gameCreation']
        times.append(gameDate)

    # Gets the current time in unix epoch time
    ms = datetime.datetime.now()
    times.append(int(time.mktime(ms.timetuple()) * 1000))

    times.sort(reverse=True)

    # Calculates time differences and appends them to diffs
    for index, i in enumerate(times):
        try:
            diffs.append(times[index] - times[index + 1])
        except IndexError:
            continue


    banked = 0
    hoursdiff = []

    # Diffs conversion
    for i in diffs:
        hoursdiff.append(i/3600000)
    sumHours = sum(hoursdiff)

    for i in range(len(hoursdiff)):
        if banked < 0: banked = 0
        if banked > 672: banked = 672

        newTime =  168 - hoursdiff[i]
        banked = banked + newTime
        if i == range(len(hoursdiff)):
            if banked < 0: banked = 0
            if banked > 672: banked = 672
            break
        if banked < 0: banked = 0
        if banked > 672: banked = 672

    banked = round(banked, 2)
    banked = banked/24

    if banked == 0.0:
        return "PLAY GAME NOW BITCH (stream that shit)"
    else:
        return f"{banked:.2f} days until decay..."
