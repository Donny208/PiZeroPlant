from TwitterClass import Twitter
from PlantClass import PlantBoxSetup
import threading
import time
import datetime

plant = PlantBoxSetup()
plant.addPin("P0", "moist_sensor", 'i', range=[1.43, 2.79])
plant.addPin(16, "servo_pump", 'o', servo=True)

#twitter consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

twitter = Twitter(ckey, csecret, atoken, asecret, plant)

def plantCheck():
    twitterRunTime = 0
    while True:
        plant.update()
        print("Soil Moisture Sensor: " + str(plant.getPinInfo("P0")['data'])+"%")
        if plant.getPinInfo("P0")['data'] < 80:
            print("Plant needs water, Turning Pump on for 5 seconds...")
            plant.outputToggle(16)
            time.sleep(5)
            print("Pump Off...")
            plant.outputToggle(16)
            twitter.tweet("Just watered.\nAt "+twitter.getFormattedTime())
        twitterRunTime = twitterRunTime + 1
        if twitterRunTime > 100:
            twitter.refresh(ckey, csecret, atoken, asecret)
            twitterRunTime = 0

        time.sleep(5)

def timelapse():
    startTime = time.time()
    while True:
        print("Timelapse Tick")
        #val = 86400.0
        val = 43200 #12 hours
        now = datetime.datetime.now() - datetime.timedelta(hours=7)
        fmt = '%m.%d.%Y_%I.%M%p'
        curTime = str(now.strftime(fmt))
        twitter.takeTimelapse(curTime)
        time.sleep(val - ((time.time() - startTime) % val))


p = threading.Thread(name='Plant Check', target=plantCheck).start()
t = threading.Thread(name='Timelapse', target=timelapse).start()
