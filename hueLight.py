import requests
import tkinter as tk
import customtkinter as ctk
import logging
import datetime
import sys

APIKEY = 'your key'
URL = 'http://your.hub.ip.addrres/api/'

logger = logging.getLogger(__name__)

class HueLight:
    def __init__(self, friendlyName, window):
        logger.info("huey init: "+friendlyName)
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
            self.btn.configure(text_color="white")
        elif isSwitchedOn == "False":
            # off so switch on:
            body = "{\"on\":true}"
            response = requests.put(url, data=body)
            self.btn.configure(fg_color="DarkOliveGreen3")
            self.btn.configure(text_color="black")
            self.btn.configure(hover_color="DarkOliveGreen3")
        elif isSwitchedOn ==  "Unavailable":
            # could do something more informative here...
            #print("Unavailable")
            self.btn.configure(fg_color="gray20")
            self.btn.configure(text_color="white")
            #self.btn.configure(hover_color="transparent")

    def convertBulbNum(self):
        #print("converting bulb name to num for ", self.friendlyName)
        if  self.friendlyName == "Living Room":
            return "/lights/2"
        elif self.friendlyName == "Donal's Room":
            return "/lights/3"
        elif self.friendlyName == "Bathroom":
            return "/lights/4"
        elif self.friendlyName == "Landing":
            return "/lights/5"
        elif self.friendlyName == "Basement":
            return "/lights/6"
            
    def buildURL(self, action):
        interMedURLString = URL + APIKEY +  str(self.bulbNum) + "/"
        #print(interMedURLString)
        if  action == "checkState":
            return interMedURLString
        # hackety hack for the new group functionality. Because the reachability is bulb-based
        # rather than group based, this is probably the best place to yeehah this
        # change in. so: checking state is based on one of the bulbs in the group;
        # switching needs a rewrite of the url.
        elif action == "switch":
            if "/6" in interMedURLString:
                interMedURLString = URL + APIKEY + "/groups/81/action"
            else:
                interMedURLString = interMedURLString + "state"
            # logger.info("switch url =" + interMedURLString)
            # if it's bulb 6: /api/KXim5vAfoi0uqGmbiMlcg0nQxyvBVooluyBhbfj8/groups/81/action
            return interMedURLString   

    def groupProcessingHack(self, url):
        logger.info("skipping group")
        try:
            response = requests.get(url)
        except:
            logger.info("group url connection failure")
            return "Unavailable"
        
    def bulbState(self):
        url= self.buildURL("checkState")

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
            #print("sad face")
            # network failure. probably true :)
            logger.info("try / catch for bulbState has failed")
            #logger.info("isSwitchedOn: ", isSwitchedOn, "; isReachable: ", isReachable)
            hubResponseForLight = "Unavailable"
        return hubResponseForLight

    def checkCurrentLightsState(self):
        isSwitchedOn = self.bulbState()
        logMsg = self.friendlyName + " switch is " + str(isSwitchedOn)
        #logger.info(logMsg)
        now = datetime.datetime.now()
        # This is to get a half hourly sample of data:
        #if now.minute == 45 or now.minute == 15:
            # disabling for now - things seem quite stable for the time being...
            # this will get a sample of data on the part that's failing. if it's time based, it may affect the results...
            # logMsg = str(now) + " " + self.friendlyName + " switch is " + str(isSwitchedOn) + "; ref count for self: " + str(sys.getrefcount(self))
            # logger.info(logMsg)
        if isSwitchedOn == "True":
            self.btn.configure(fg_color="DarkOliveGreen3")
            self.btn.configure(bg_color="DarkOliveGreen3")
            self.btn.configure(text_color="black")
        elif isSwitchedOn == "False":
            self.btn.configure(fg_color="firebrick3")
            self.btn.configure(fg_color="firebrick3")
            self.btn.configure(text_color="white")
        elif isSwitchedOn == "Unavailable":
            self.btn.configure(fg_color="gray20")
            self.btn.configure(bg_color="gray20")
            self.btn.configure(text_color="white")
        self.btn.after(15000, self.checkCurrentLightsState)
