import requests
from bs4 import BeautifulSoup
import feedparser
import customtkinter as ctk
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class Iod:
    def __init__(self, targetSite):
        self.targetSite = targetSite

    def downloadImg(self):
        if self.targetSite == "Nasa":
            nasaPage = requests.get("https://apod.nasa.gov/apod/astropix.html")
            soup = BeautifulSoup(nasaPage.content, "html.parser")
            result = str(soup.find("img"))
            #print(result)
            indexLeft = result.find("src=\"")
            leftTrunc= result[indexLeft+5:]
            indexRight = leftTrunc.find("\" style")
            rightTrunc =  leftTrunc[:indexRight]
            #print(rightTrunc)
            dailyURL = "https://apod.nasa.gov/apod/"+rightTrunc
            #print(dailyURL)
        elif self.targetSite == "wikiCommons":
            feed = feedparser.parse("https://commons.wikimedia.org/w/api.php?action=featuredfeed&feed=potd&feedformat=rss&language=en")
            html = feed.entries[-1].description
            #print(html)
            indexLeft = html.find("src=\"")
            leftTrunc = html[indexLeft+5:]
            #print("left trunc: ", leftTrunc)
            indexRight = leftTrunc.find("jpg\"")
            dailyURL = leftTrunc[:indexRight+3]
        try: 
            response = requests.get(dailyURL)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                width = img.width
                height = img.height
                if width > img.height:
                    imgType = "landscape"
                else:
                    imgType = "portrait"
                return img, imgType
        except:
            logger.info("Nasa IOD call failed:")
            logger.info("dailyURL: "+dailyURL)
            logger.info("response code: "+response.status_code)
            # the quit is temporary to see if this is the problem.
            # the graceful thing to do would be to load a 'blank' img from file and return that.
            quit()
            
    def resizeImg(self, img, imgType):
        newWidth = 0
        newHeight = 0
        #logger.info("imgType: "+imgType+"; img.width: "+str(img.width)+"; img.height: "+str(img.height))
        # 525 x 350 isn't a standard 16:9 ratio. then again, the nasa pics aren't standard either

        if imgType == "portrait":
            widthRatio = 350 / img.height
            newWidth = widthRatio * img.width
            newHeight = 350
        elif imgType == "landscape":
            # actual height (possibly non standard) / 350 = heightResizeRatio
            widthResizeRatio= img.height / 350
            logger.info("widthResizeRatio: "+str(widthResizeRatio))
            newWidth = img.width / widthResizeRatio
            logger.info("newWidth: "+str(newWidth))
            newHeight = 350
        return newWidth, newHeight


    
    def getImage(self):
        img = None
        (img, imageType) = self.downloadImg()

        if (img.width > 525) or (img.height > 350):
            (newWidth, newHeight) = self.resizeImg(img, imageType)
            return ctk.CTkImage(img, size=(newWidth, newHeight))
        else:
            return ctk.CTkImage(img, size=(img.width, img.height))

