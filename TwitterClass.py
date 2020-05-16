import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from CameraClass import Camera
import datetime

class Twitter:
    def __init__(self, ckey, csecret, atoken, asecret, plant=False):
        self.auth = OAuthHandler(ckey, csecret)
        self.auth.set_access_token(atoken, asecret)
        self.api = tweepy.API(self.auth)
        self.twitterStream = Stream(self.auth, self.listener(self))
        self.twitterStream.filter(track=['@literally_plant'], is_async=True)
        self.plant = plant
        self.camera = Camera()

    def tweet(self, msg):
        self.api.update_status(msg)

    class listener(StreamListener):
        def __init__(self,tObj):
            self.tObj = tObj

        def on_data(self, data):
            data = json.loads(data)
            dataDict = {
                'id':       data['id'],
                'text':     data['text'],
                'user':{
                    'name':         data['user']['name'],
                    'screen_name':  data['user']['screen_name']
                }

            }

            print("Tweet Received By: @"+dataDict['user']['screen_name']+" - "+dataDict['text'])

            if "moist" in dataDict['text'] and "?" in dataDict['text']:
                print("Sending Moisture Level...")
                self.tObj.api.update_status("@"+dataDict['user']['screen_name']+" Soil Moisture: "+str(self.tObj.plant.getPinInfo("P0")['data'])+"%\nAt "+self.tObj.getFormattedTime(), in_reply_to_status_id = dataDict['id'])
            elif "picture" in dataDict['text'] and "?" in dataDict['text']:
                print("Sending Picture...")
                filename = "./img/pic.jpg"
                self.tObj.camera.takePhoto(filename)
                self.tObj.api.update_with_media(filename, status="@"+dataDict['user']['screen_name']+" Picture taken at "+self.tObj.getFormattedTime()+"\nDay: "+str(abs((datetime.datetime.today()-self.tObj.plant.startDate).days)), in_reply_to_status_id = dataDict['id'])

        def on_error(self, status):
            print(status)

    def refresh(self, ckey, csecret, atoken, asecret):
        print("Refreshing Credentials...")
        self.auth = OAuthHandler(ckey, csecret)
        self.auth.set_access_token(atoken, asecret)
        self.api = tweepy.API(self.auth)
        # self.twitterStream = Stream(self.auth, self.listener(self))
        # self.twitterStream.filter(track=['@literally_plant'], is_async=True)

    def getFormattedTime(self):
        now = datetime.datetime.now() - datetime.timedelta(hours=7)
        fmt = '%I:%M:%S%p MDT %m/%d/%Y'

        return str(now.strftime(fmt))

    def takeTimelapse(self, filename):
        print("Taking Timelapse Picture...")
        filename = "./timelapse/"+filename+".jpg"
        self.camera.takePhoto(filename)
        self.api.update_with_media(filename, status="Timelapse picture taken at " + self.getFormattedTime() + "\nDay: " + str(abs((datetime.datetime.today() - self.plant.startDate).days)))