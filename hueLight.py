import requests
import tkinter as tk
import customtkinter as ctk
import logging
import datetime
import sys

APIKEY = 'your key here'
URL = 'http://192.168.0.4/api/'

logger = logging.getLogger(__name__)

class HueLight:
    def __init__(self, friendlyName, window):
        logger.info("huey init: "+friendlyName)
        self.friendlyName = friendlyName
        self.bulbNum = self.convertBulbNum()
        self.friendlyName = friendlyName
        self.btn = ctk.CTkButton(window, text = friendlyName, font=("Callibri", 20), command = lambda: self.toggleLight(), width=140, height=60)

    def toggleLight(self):
        logger.info("toggleLight")
        isSwitchedOn = self.bulbState()
        #logger.info("isSwitchedOn: ", isSwitchedOn)
        url= self.buildURL("switch")
        if isSwitchedOn == "True":
            body = "{\"on\":false}"
            response = requests.put(url, data=body)
            self.btn.configure(fg_color="firebrick3")
            self.btn.configure(hover_color="firebrick3")
        elif isSwitchedOn == "False":
            # off so switch on:
            body = "{\"on\":true}"
            response = requests.put(url, data=body)
            self.btn.configure(fg_color="DarkOliveGreen3")
            #self.btn.configure(bg_color="DarkOliveGreen3")
            self.btn.configure(hover_color="DarkOliveGreen3")
        elif isSwitchedOn ==  "Unavailable":
            # could do something more informative here...
            #print("Unavailable")
            self.btn.configure(fg_color="gray20")
            #self.btn.configure(hover_color="transparent")

    def convertBulbNum(self):
        #print("converting bulb name to num for ", self.friendlyName)
        if  self.friendlyName == "Living Room":
            return 2
        elif self.friendlyName == "Donal's Room":
            return 3
        elif self.friendlyName == "Bathroom":
            return 4
        elif self.friendlyName == "Landing":
            return 5
        elif self.friendlyName == "Dining Room":
            return 6
            
    def buildURL(self, action):
        interMedURLString = URL + APIKEY + "/lights/" + str(self.bulbNum) + "/"
        #print(interMedURLString)
        if  action == "checkState":
            return interMedURLString
        elif action == "switch":
            return interMedURLString + "state"        

    def bulbState(self):
        url= self.buildURL("checkState")
        # this has evolved; could do with a tidy up:
        try:
            response = requests.get(url)
        except:
            # response = "connection failure"
            logger.info("bulb state hub connection failure")
            hubResponseForLight = "Unavailable"
            return hubResponseForLight
        #if response != "connection failure":
        try:
            jsonData = response.json()
        except:
            logger.info("bulb state json parsing failure")
            hubResponseForLight = "Unavailable"
            return hubResponseForLight
        #logger.info(jsonData)
        try:
            # weird: the json value is prefixed with a space...
            isSwitchedOn = str(jsonData['state']['on']).strip()
            isReachable = str(jsonData['state']['reachable']).strip()
            #logger.info(self.friendlyName+": isSwitchedOn: "+isSwitchedOn+"; isReachable: "+isReachable)
            if isSwitchedOn == "True" and isReachable == "True":
                hubResponseForLight = "True"
            elif isSwitchedOn == "False" and isReachable == "True":
                hubResponseForLight = "False"
            # this takes about 30 seconds to filter through:
            elif isReachable == "False":
                hubResponseForLight = "Unavailable"
            else: 
                logger.info("bulbState json had unexpected values: \n"+ jsonData)
                #print("also sad face")
        except:
            # network failure. probably true :)
            logger.info("try / catch for bulbState has failed")
            logger.info("isSwitchedOn: ", isSwitchedOn, "; isReachable: ", isReachable)
            hubResponseForLight = "Unavailable"
        return hubResponseForLight

    def checkCurrentLightsState(self):
        isSwitchedOn = self.bulbState()
        logMsg = self.friendlyName + " switch is " + str(isSwitchedOn)
        #logger.info(logMsg)
        now = datetime.datetime.now()
        # This is to get a half hourly sample of data:
        if now.minute == 45 or now.minute == 15:
            logMsg = str(now) + " " + self.friendlyName + " switch is " + str(isSwitchedOn) + "; ref count for self: " + str(sys.getrefcount(self))
            logger.info(logMsg)
        if isSwitchedOn == "True":
            self.btn.configure(fg_color="DarkOliveGreen3")
            self.btn.configure(bg_color="DarkOliveGreen3")
        elif isSwitchedOn == "False":
            self.btn.configure(fg_color="firebrick3")
            self.btn.configure(fg_color="firebrick3")
        elif isSwitchedOn == "Unavailable":
            self.btn.configure(fg_color="gray20")
            self.btn.configure(bg_color="gray20")
        self.btn.after(15000, self.checkCurrentLightsState)
