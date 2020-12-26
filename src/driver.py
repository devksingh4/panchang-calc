from panchang import tithi, gregorian_to_jd, Place, Date
from datetime import date, timedelta
import time, json, schedule, sys

today =  date.fromtimestamp(time.time())
nextAmavasya = None

def getTithiNum(jd, place):
    return tithi(jd, place)[0]
def getLocationInfo(cityName):
    with open('cities.json') as f:
        data = json.load(f)
        return data[cityName]
def getNextAmavasya(loc=Place(41.8781, 87.6298, -6)):
    tithiNum = getTithiNum(gregorian_to_jd(Date(today.year, today.month, today.day)), loc)
    i = 0
    err = False
    while tithiNum != 30:
        i += 1
        currDate = today + timedelta(days=i)
        currJd = gregorian_to_jd(Date(currDate.year, currDate.month, currDate.day))
        tithiNum = getTithiNum(currJd, loc)
        i += 1
        if i > 31: 
            print("[ERR] An error occured and the next Amavasya could not be found.")
            err = True
            break
    global nextAmavasya
    if not err:
        nextAmavasya = today + timedelta(days=i - 1)
    else:
        nextAmavasya = None
print("[INFO] Starting daemon...")
schedule.every().day.at("02:00").do(getNextAmavasya)
print("[INFO] Started!")
while True:
    try:
        oldAmavasya = nextAmavasya
        schedule.run_pending()
        time.sleep(1)
    except: 
        print("[INFO] Daemon stopped!")
        sys.exit(1)