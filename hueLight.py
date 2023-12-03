import requests
import tkinter as tk
import customtkinter as ctk
import logging
import datetime
import time

APIKEY = 'goes here'
URL = 'http://192.168.0.4/api/'
logger = logging.getLogger(__name__)


class HueLight:
    def __init__(self, friendlyName, window):
        self.friendlyName = friendlyName
        self.bulbNum = self.convertBulbNum()
        self.friendlyName = friendlyName
        self.btn = ctk.CTkButton(window, text = friendlyName, font=("Callibri", 20), command = lambda: self.toggleLight(), width=140, height=60)

    def toggleLight(self):
        #logger.info("toggleLight")
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
        response = requests.get(url)
        try:
            jsonData = response.json()
        except:
            logger.info("Endpoint didn't return valid json")
            logger.info(response)
            hubResponseForLight = "unavailable"
            return hubResponseForLight
        hubResponseForLight = ""
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
        except:
            # network failure. probably true :)
            logger.info("try / catch for bulbState has failed")
            logger.info("isSwitchedOn: ", isSwitchedOn, "; isReachable: ", isReachable)
            hubResponseForLight = "Unavailable"
        return hubResponseForLight

    def checkCurrentLightsState(self):
        isSwitchedOn = self.bulbState()
        now = datetime.datetime.now()
        # This is to get an hourly sample of data:
        if now.minute == 45 and now.second > 30:
            # this will get a sample of data on the part that's failing. if it's time based, it may affect the results...
            logMsg = self.friendlyName + " switch is " + str(isSwitchedOn)
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
        self.btn.after(10000, self.checkCurrentLightsState)

