import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import numpy as np
import neopixel
import time
from adafruit_mcp3xxx.analog_in import AnalogIn
import datetime

# GPIO setup
GPIO.setmode(GPIO.BCM)

class PlantBoxSetup:
    def __init__(self):
        self.pinData = {}
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(board.D5)
        self.mcp = MCP.MCP3008(self.spi, self.cs)
        self.startDate = datetime.datetime(2020, 5, 14)
        self.mcpPins = {
            'P0': MCP.P0,
            'P1': MCP.P1,
            'P2': MCP.P2,
            'P3': MCP.P3,
            'P4': MCP.P4,
            'P5': MCP.P5,
            'P6': MCP.P6,
            'P7': MCP.P7,
        }
        self.boardPins = {
            'D18': board.D18
        }

        ###########
        ##Modules##
        ###########

        #W2LED
        self.pixels = None
        self.ledNum = None

    def addPin(self, pin, name, type, range=None, servo=False):
        self.pinData[str(pin)] = {
            'name':             name,
            'type':             type,
            'rawData':             -1,
            'data':             -1,
            'range':            range,
            'servo':            servo
        }
        if type == 'o' and "servo" in name:
            GPIO.setup(pin, GPIO.OUT) #todo, not sure on this one
            GPIO.output(pin, GPIO.HIGH)
            self.pinData[str(pin)]['data'] = GPIO.HIGH

    def getAllPinData(self):
        return str(self.pinData)

    def getPinInfo(self, pin):
        return self.pinData[str(pin)]

    def outputOff(self, pin):
        print("Pin "+str(pin)+" Is Now Off\n")
        if self.pinData[str(pin)]['type'] == 'o' and self.pinData[str(pin)]['servo'] == False:
            GPIO.output(pin, GPIO.LOW)
            self.pinData[str(pin)]['data'] = GPIO.LOW
        elif self.pinData[str(pin)]['type'] == 'o' and self.pinData[str(pin)]['servo'] == True:
            GPIO.output(pin, GPIO.HIGH)
            self.pinData[str(pin)]['data'] = GPIO.HIGH

    def outputOn(self, pin):
        print("Pin " + str(pin) + " Is Now On\n")
        if self.pinData[str(pin)]['type'] == 'o' and self.pinData[str(pin)]['servo'] == False:
            GPIO.output(pin, GPIO.HIGH)
            self.pinData[str(pin)]['data'] = GPIO.HIGH
        elif self.pinData[str(pin)]['type'] == 'o' and self.pinData[str(pin)]['servo'] == True:
            GPIO.output(pin, GPIO.LOW)
            self.pinData[str(pin)]['data'] = GPIO.LOW

    def outputToggle(self, pin):
        print("Pin " + str(pin) + " Is Now Toggled\n")
        if self.pinData[str(pin)]['type'] == 'o':
            if self.pinData[str(pin)]['data']== GPIO.LOW:
                GPIO.output(pin, GPIO.HIGH)
                self.pinData[str(pin)]['data'] = GPIO.HIGH
            else:
                GPIO.output(pin, GPIO.LOW)
                self.pinData[str(pin)]['data'] = GPIO.LOW

    def formatData(self, pin, data):
        if self.pinData[str(pin)]['name'] == 'moist_sensor':
            self.pinData[str(pin)]['data'] = round(np.interp(data,self.pinData[str(pin)]['range'],[100,0]),3)

    def update(self):
        for key, value in self.pinData.items():
            #print(key+ ": "+value['type'])

            #Digital Value
            if value['type'] == 'i' and key[0] != "P":
                prsint("Digital")

            #Analog Value
            elif value['type'] == 'i' and key[0] == "P":
                #print("Analog")
                self.pinData[key]['rawData'] = AnalogIn(self.mcp, self.mcpPins[str(key)])
                self.formatData(key, self.pinData[key]['rawData'].voltage)

    ############
    ##MODDULES##
    ############

    ##W2LED##

    def w2ledAdd(self, pin, ledNum):
        self.pixels = neopixel.NeoPixel(self.boardPins[pin], ledNum)
        self.ledNum = ledNum
        self.addPin("D18", "w2led", 'o')

    def w2ledSet(self, rgb):
        for x in range(0,74):
                #pixels[x] = (255,20,147)
                self.pixels[x] = (rgb[0], rgb[1], rgb[2])

