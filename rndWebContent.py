import requests
import tkinter as tk
import customtkinter as ctk
import feedparser
import random
from bs4 import BeautifulSoup
from PIL import Image
from googleCalendar import GoogleCalendar

class RndWebContent:
    def __init__(self, webLbl, screenTitle):
        self.webLbl = webLbl
        self.title = screenTitle
    def buildLabel(self):
        rndResult = ""
        contentChoice = random.randint(0,6)
        #contentChoice = 6
        print("contentChoice: ", contentChoice)
        if contentChoice == 0:
            rndResult=self.getRSSContent("http://feeds.bbci.co.uk/news/rss.xml", 8)
            #print("0: rndResult: ", rndResult)
            self.webLbl.configure(text=rndResult)
            self.title.configure(text="BBC News Headlines")
            self.webLbl.configure(image="")
        elif contentChoice == 1:
            rndResult=self.getRSSContent("https://feeds.skynews.com/feeds/rss/world.xml", 7)
            #print("1: rndResult: ", rndResult)
            self.webLbl.configure(text=rndResult)
            self.title.configure(text="Sky News World Headlines")
            self.webLbl.configure(image="")
        elif contentChoice == 2:
            rndResult=self.getRSSContent("http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/front_page/rss.xml", 8)
            #print("2: rndResult: ", rndResult)
            self.webLbl.configure(text=rndResult)
            self.title.configure(text="BBC Sport Headlines")
            self.webLbl.configure(image="")
        elif contentChoice == 3:
            # rndResult=self.threeDayBeebForcast()
            rndResult=self.getRSSContent("https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/sixDigitCodeForYourTownHere", 3)
            self.webLbl.configure(text=rndResult)
            self.title.configure(text="BBC 3 Day Weather for Wherever")
            self.webLbl.configure(image="")
        elif contentChoice == 4:
            self.getNasaIOD()
            img = ctk.CTkImage(Image.open('daily.jpg'), size=(442,347))
            LabelIMG = img 
            self.webLbl.configure(image=LabelIMG)
            self.title.configure(text="NASA Image of the Day")
            self.webLbl.configure(text="")
        elif contentChoice == 5:
            rndResult=self.getRSSContent("https://www.cambridge-news.co.uk/?service=rss", 5)
            self.webLbl.configure(text=rndResult)
            self.title.configure(text="Cambridge News")
            self.webLbl.configure(image="")
        elif contentChoice == 6:
            cal = GoogleCalendar()
            eventsString = cal.getEvents()
            self.webLbl.configure(text=eventsString)
            self.title.configure(text="Upcoming Calendar Events")
            self.webLbl.configure(image="")
        #15 mins = 900000
        self.webLbl.after(900000, self.buildLabel)

    def getNasaIOD(self):
        nasaPage = requests.get("https://apod.nasa.gov/apod/astropix.html")
        soup = BeautifulSoup(nasaPage.content, "html.parser")
        result = str(soup.find("img"))
        #print(result)
        indexLeft = result.find("src=\"")
        leftTrunc= result[indexLeft+5:]
        indexRight = leftTrunc.find("\" style")
        rightTrunc =  leftTrunc[:indexRight]
        print(rightTrunc)
        dailyURL = "https://apod.nasa.gov/apod/"+rightTrunc
        print(dailyURL)
        response = requests.get(dailyURL)
        if response.status_code == 200:
            with open("daily.jpg", 'wb') as f:
                f.write(response.content)

    def getRSSContent(self, url, count):
        labelString=""
        feed = feedparser.parse(url)
        for x in range(0,count):
            print(feed.entries[x].title, len(feed.entries[x].title))
            headlineString = feed.entries[x].title
            headlineString = self.stringCheckAndTrunc(headlineString,95)
            labelString += headlineString+"\n"
            #print(headlineString)
        print("getRSSContent: ", labelString)
        return labelString
    
    def stringCheckAndTrunc(self, inString, maxLength):
        if (len(inString) > maxLength):
            inString = (inString[0:maxLength-3]+"...")
        return inString
        
