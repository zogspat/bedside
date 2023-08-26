import requests
import tkinter as tk
import customtkinter as ctk

APIKEY = 'yourKeyHere'
URL = 'http://yourHueHubAddressHere'


class HueLight:
    def __init__(self, friendlyName, window):
        self.friendlyName = friendlyName
        self.bulbNum = self.convertBulbNum()
        self.friendlyName = friendlyName
        self.btn = ctk.CTkButton(window, text = friendlyName, font=("Callibri", 20), command = lambda: self.toggleLight(), width=140, height=60)

    def toggleLight(self):
        switchPosn = self.bulbState()
        #print("switch pos is ", switchPosn)
        url= self.buildURL("switch")
        if switchPosn == "True":
            #on now so swtich off:
            #print("***** on so now off....!!!")
            body = "{\"on\":false}"
            response = requests.put(url, data=body)
            self.btn.configure(fg_color="firebrick3")
            #self.btn.configure(bg_color="firebrick3")
            self.btn.configure(hover_color="firebrick3")
        elif switchPosn == "False":
            # off so switch on:
            body = "{\"on\":true}"
            response = requests.put(url, data=body)
            self.btn.configure(fg_color="DarkOliveGreen3")
            #self.btn.configure(bg_color="DarkOliveGreen3")
            self.btn.configure(hover_color="DarkOliveGreen3")
        elif switchPosn ==  "Unavailable":
            # could do something more informative here...
            #print("Unavailable")
            self.btn.configure(fg_color="black")
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
        jsonData = response.json()
        #print(jsonData)
        try:
            # weird: the json value is prefixed with a space...
            isSwitchedOn = str(jsonData['state']['on']).strip()
        except:
            isSwitchedOn = "Unavailable"
        #print("in bulbState for ", self.friendlyName, " and bulb on is ", isSwitchedOn)
        return isSwitchedOn

    def checkCurrentLightsState(self):
        switchPosn = self.bulbState()
        print(self.friendlyName, "switch is ", switchPosn)
        if switchPosn == "True":
            #print("on")
            self.btn.configure(fg_color="DarkOliveGreen3")
            self.btn.configure(bg_color="DarkOliveGreen3")
            #light.btn.configure(hover_color="transparent")
        elif switchPosn == "False":
            #print("off")
            self.btn.configure(fg_color="firebrick3")
            self.btn.configure(fg_color="firebrick3")
            #light.btn.configure(hover_color="transparent")
        elif switchPosn == "Unavailable":
            #print("Unavailable")
            self.btn.configure(fg_color="black")
            #light.btn.configure(hover_color="transparent")
        self.btn.after(10000, self.checkCurrentLightsState)
