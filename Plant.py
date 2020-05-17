#!/usr/bin/python3

from TwitterClass import Twitter
from PlantClass import PlantBoxSetup
import threading
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

plant = PlantBoxSetup()
plant.addPin("P0", "moist_sensor", 'i', range=[1.43, 2.79])
plant.addPin(16, "servo_pump", 'o', servo=True)

#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

twitter = Twitter(ckey, csecret, atoken, asecret, plant)

sched = BackgroundScheduler({'apscheduler.timezone':  'America/Denver'})

def plantCheck():
    twitterRunTime = 0
    while True:
        plant.update()
        print("Soil Moisture Sensor: " + str(plant.getPinInfo("P0")['data'])+"%")
        if plant.getPinInfo("P0")['data'] < 85:
            print("Plant needs water, Turning Pump on for 5 seconds...")
            plant.outputToggle(16)
            time.sleep(2.5)
            print("Pump Off...")
            plant.outputToggle(16)
            twitter.tweet("Just watered.\nAt "+twitter.getFormattedTime())
        twitterRunTime = twitterRunTime + 1
        if twitterRunTime > 100:
            twitter.refresh(ckey, csecret, atoken, asecret)
            twitterRunTime = 0

        time.sleep(5)

def timelapse():
    print("Timelapse Tick")
    now = datetime.datetime.now() - datetime.timedelta(hours=7)
    fmt = '%m.%d.%Y_%I.%M%p'
    curTime = str(now.strftime(fmt))
    twitter.takeTimelapse(curTime)


p = threading.Thread(name='Plant Check', target=plantCheck).start()
#t = threading.Thread(name='Timelapse', target=timelapse).start()
sched.add_job(timelapse, 'cron', day_of_week='mon-sun', hour=20)
sched.add_job(timelapse, 'cron', day_of_week='mon-sun', hour=8)
##For Reference##
##hour 20 - 8PM
##hour 8 - 8AM
################
sched.start()
