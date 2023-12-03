import requests
import tkinter as tk
import customtkinter as ctk
import feedparser
import random
from bs4 import BeautifulSoup
from PIL import Image
from googleCalendar import GoogleCalendar
from iod import Iod
import logging

logger = logging.getLogger(__name__)

class RndWebContent:
    def __init__(self, webLbl, screenTitle):
        self.webLbl = webLbl
        self.title = screenTitle
    def buildLabel(self):
        rndResult = ""
        contentChoice = random.randint(0,6)
        # contentChoice = 7
        print("contentChoice: ", contentChoice)
        if contentChoice == 0:
            rndResult=self.getRSSContent("http://feeds.bbci.co.uk/news/rss.xml", 8)
            self.webLbl.configure(text=rndResult)
            self.title.configure(text="BBC News Headlines")
            self.webLbl.configure(image="")
        elif contentChoice == 1:
            rndResult=self.getRSSContent("https://feeds.skynews.com/feeds/rss/world.xml", 6)
            self.webLbl.configure(text=rndResult)
            self.title.configure(text="Sky News World Headlines")
            self.webLbl.configure(image="")
        elif contentChoice == 2:
            rndResult=self.getRSSContent("http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/front_page/rss.xml", 6)
            self.webLbl.configure(text=rndResult)
            self.title.configure(text="BBC Sport Headlines")
            self.webLbl.configure(image="")
        elif contentChoice == 3:
            rndResult=self.getRSSContent("https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/2646393", 3)
            self.webLbl.configure(text=rndResult)
            self.title.configure(text="BBC 3 Day Weather for Huntingdon")
            self.webLbl.configure(image="")
        elif contentChoice == 4:
            iodImage = Iod("Nasa")
            img = iodImage.getImage()
            LabelIMG = img 
            self.webLbl.configure(image=LabelIMG)
            self.title.configure(text="Nasa Image of the Day")
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
        elif contentChoice == 7:
            # the parsing of the HTML is proving unreliable so not calling this. May revisit...
            iodImage = Iod("wikiCommons")
            img = iodImage.getImage()
            LabelIMG = img 
            self.webLbl.configure(image=LabelIMG)
            self.title.configure(text="Wiki Commons Image of the Day")
            self.webLbl.configure(text="")
        #15 mins = 900000
        self.webLbl.after(600000, self.buildLabel)

    def getRSSContent(self, url, count):
        labelString=""
        try:
            feed = feedparser.parse(url)
            for x in range(0,count):
                print(feed.entries[x].title, len(feed.entries[x].title))
                headlineString = feed.entries[x].title
                headlineString = self.stringCheckAndTrunc(headlineString,95)
                labelString += headlineString+"\n"
                #print(headlineString)
        except:
            logger.info("feedparser failed for "+url)
            labelString = url+"\n"+"Unhappy at the moment.\nMaybe try later...?"
        return labelString
    
    def stringCheckAndTrunc(self, inString, maxLength):
        if (len(inString) > maxLength):
            inString = (inString[0:maxLength-3]+"...")
        return inString
        
