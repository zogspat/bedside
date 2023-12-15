from hueLight import HueLight
import customtkinter as ctk
import time
import requests
from rndWebContent import RndWebContent
from PIL import Image
# for some reaon this isn't working:
# from rpi_backlight import Backlight
import logging
import os

#logger = logging.getLogger(__name__)
logging.basicConfig(filename='/home/zog/bedside/bedside.log', level=logging.INFO)
logging.info("logging.info: In bedside.py")

window = ctk.CTk()
window.attributes('-fullscreen', True)
window.geometry('800x480')

# might as well pass these around too:
livingRoomLight = HueLight("Living Room", window)
dhBedroomLight = HueLight("Donal's Room", window)
bathRoomLight = HueLight("Bathroom", window)
landingLight = HueLight("Landing", window)
diningRoomLight = HueLight("Dining Room", window)

clockLbl = ctk.CTkLabel(window, width=150, height=50, bg_color=("transparent"), fg_color=("transparent"), font=("Callibri", 40))
#bl = Backlight()
weatherLbl = ctk.CTkLabel(window, width=350, height=40, bg_color=("transparent"), fg_color=("transparent"), font=("Callibri", 30))
webLbl = ctk.CTkLabel(window, width=750, height=350, justify="left", wraplength=700, bg_color=("transparent"), fg_color=("transparent"), font=("Callibri", 20))
screenTitle = ctk.CTkLabel(window, width=250, height=35, justify="center", bg_color=("transparent"), fg_color=("transparent"), font=("Callibri", 25))
#img = Image.open('offBtn.JPG')
#ctkImgKillBtn = ctk.CTkImage(img, size=(50,46))
killBtn = ctk.CTkButton(window, width=50, height=46, fg_color=("red"), hover="False", bg_color=("red"), command=window.destroy, font=("Callibri", 30), text="X")

def placeLightControlBtns():
    livingRoomLight.btn.place(x=10, y=410)
    dhBedroomLight.btn.place(x=165, y=410)
    bathRoomLight.btn.place(x=330, y=410)
    landingLight.btn.place(x=485, y=410)
    diningRoomLight.btn.place(x=640, y=410)

def checkTime():
    dateTimeDisplayString = time.strftime('%d/%m    %H:%M %p')
    timeCheckString = time.strftime("%H:%M")
    #logger.info(timeCheckString)
    if timeCheckString == "22:00":
        #logger.info("it's 10pm")
        #bl.brightness = 20
        os.system("rpi-backlight -b 20")
    elif timeCheckString == "23:00":
        #logger.info("it's 11pm")
        #bl.brighness = 5
        os.system("rpi-backlight -b 5")
    elif timeCheckString == "08:00":
        #bl.brighness = 100
        os.system("rpi-backlight -b 100")
    #else:
    #    logger.info("none of the above")
    clockLbl.configure(text=dateTimeDisplayString)
    clockLbl.after(30000, checkTime)
    #clockLbl.after(10000, time)


def weatherCheck():
   apiKey="your key here"
   apiURL="https://api.openweathermap.org/data/2.5/weather?lat=52.33&lon=-0.179&units=metric&appid="+apiKey
   response = requests.get(apiURL)
   data = response.json()
   weatherString = str(data['main']['temp'])+'\xb0C, '+ data['weather'][0]['main']
   weatherLbl.configure(text=weatherString)
   weatherLbl.after(10800000, weatherCheck)

#not using but leaving for now
#def screenShot():
#    options = Options()
#    #options.add_argument('headless')
#    options.add_argument('window-size=2048,1000')
#    driver = webdriver.Chrome(options=options)  # Optional argument, if not specified will search path.
#    driver.get('https://bbc.co.uk/news')
#    driver.save_screenshot('my_screenshot.png')
#    driver.quit()
#    img = Image.open('my_screenshot.png')
#    # this has to keep the same ratio as the window size - it doesn't atm:
#    beebArea = (400,80,2000,1000)
#    cropped = img.crop(beebArea)
#    resized = cropped.resize((750,341))
#    labelImg = ctk.CTkImage(resized, size=(750,300))
#    webLbl.place(x=15,y=60)mainLabelContent = RndWebContent(webLbl)
#    webLbl.configure(image=labelImg)

def main():
    ctk.set_appearance_mode("dark")
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('main started...')
    allLights = [livingRoomLight, dhBedroomLight, bathRoomLight, landingLight, diningRoomLight]
    for light in allLights:
        light.checkCurrentLightsState()
        #time.sleep(1)
    placeLightControlBtns()
    screenTitle.place(x=180,y=60)
    clockLbl.place(x=0, y=10)
    checkTime()
    weatherLbl.place(x=433, y=10)
    weatherCheck()
    webLbl.place(x=10,y=60)
    #webContent()
    mainLabelContent = RndWebContent(webLbl, screenTitle)
    mainLabelContent.buildLabel()
    killBtn.place(x=750,y=0)
    window.mainloop()

if __name__ == "__main__":
    main()
