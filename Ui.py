# -*- coding: utf-8 -*-
from tkinter import *
from exchanges.bitfinex import Bitfinex
from bs4 import BeautifulSoup
import urllib2
import forecastio
import time
from PIL import ImageTk, Image,ImageFont, ImageDraw
import feedparser
import json
import freenect
import numpy as np


obj_distance = 100
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
public_images = []
import smtplib
import time
import imaplib
import email
BASELINE_DEPTH = 80
LEFT_SIDE = 1
ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "maxnorman.biz" + ORG_EMAIL
FROM_PWD    = "Maxnor22"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 465

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
def get_depth():
    array, _ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    checker = 0
    for x in range(150, 350):
        for y in range(150, 350):
            if (array[x][y] >= BASELINE_DEPTH):
                checker += 1

    if checker >= (200 * 200) / 2:
        addBtc()
        addHashRate()
        addNewsFeed()
        print "aa"
        images = putWeatherOnScreen()

def read_email_from_gmail():
    endArr = []
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])


        for i in range(latest_email_id,latest_email_id - 5, -1):
            typ, data = mail.fetch(i, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    endArr.append(email_from)
                    endArr.append(email_subject)

    except Exception, e:
        print str(e)
    return endArr
cnnUS = "http://rss.cnn.com/rss/cnn_us.rss"
cnntech = "http://rss.cnn.com/rss/cnn_tech.rss"
slushUrl = "https://slushpool.com/accounts/profile/json/1787598-f474765ec374ff7e6ea8695635f1415f"
def add_images_to_public():
    size = 60, 60
    list_of_things = ["Sunny", "Cloudy", "Rain", "Moon", "Snow"]
    for c in list_of_things:
        ab = Image.open(getImage(c))
        ab.thumbnail(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(ab)
        public_images.append(photo)

def get_thumbnails(a):
    str(a)
    if int(time.strftime("%H")) > 6:
        if "Cloudy" in a:
            return public_images[1]
        elif "Rain" in a:
            return public_images[2]
        elif "Sunny" in a:
            return public_images[3]
        elif "Snow" in a:
            return public_images[4]
        else:
            return public_images[3]
    else:
        if "Cloudy" in a:
            return public_images[1]
        elif "Rain" in a:
            return public_images[2]
        elif "Sunny" in a:
            return public_images[0]
        elif "Snow" in a:
            return public_images[4]
        else:
            return public_images[0]

def parseRSS( rss_url ):
    return feedparser.parse( rss_url )
def getHeadlines(rss_url):
    headlines = []

    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])

    return headlines
def getBtc():
    return ("The Value of Bitcoin is: " + str(round(Bitfinex().get_current_price(),2)) + "USD")
def getSlushPool():
    url = urllib2.urlopen(slushUrl)
    soup = BeautifulSoup(url)
    return json.loads(soup.text)
def addHashRate():
    a = getSlushPool()
    hr = float(a["hashrate"])
    hr /=1000000
    hr = round(hr,2)
    r = float(a["confirmed_reward"])
    r = float(Bitfinex().get_current_price())* r
    r = round(r,2)
    Label(text=("Hashrate: " + str(hr)+ " Th/s"),bd = 2, fg = "white", bg = "black",anchor = "nw", width = 50, font = ("Helvetica Neue light", 20)).place(x= LEFT_SIDE, y = 25)
    Label(text=("Reward: $" + str(r)),bd = 2, fg="white", bg="black",anchor = "nw", width=50, font=("Helvetica Neue light", 20)).place(x= LEFT_SIDE, y = 49)
def convertTime(a):
    b = a + 4
    print b
    if b > 12:
        b %= 12
    return str (b) + ":00"
def convertTemp(a):
    return str(int(round(a, 0))) + "°"
def getWeather():
    endArr = [[]]
    api_key = "47511347a1715bbb2c2c1be59f5184c3"
    lat = 45.524366
    lng = -123.110589
    forecast = forecastio.load_forecast(api_key, lat, lng)
    byHour = forecast.hourly()
    counter = 0
    for hourlyData in byHour.data:

        arr = []

        arr.append(convertTime(hourlyData.time.hour))
        arr.append(convertTemp(hourlyData.temperature))
        arr.append(hourlyData.summary)
        endArr.append(arr)
    return endArr
def getImage(a):
    str(a)
    if int(time.strftime("%H")) > 6:
        if "Cloudy" in a:
            return 'cloudy.jpeg'
        elif "Rain" in a:
            return 'rainy.jpeg'
        elif "Sunny" in a:
            return "moon.jpeg"
        elif "Snow" in a:
            return "snowy.jpeg"
        else:
            return "moon.jpeg"
    else:
        if "Cloudy" in a:
            return 'cloudy.jpeg'
        elif "Rain" in a:
            return 'rainy.jpeg'
        elif "Sunny" in a:
            return "moon.jpeg"
        elif "Snow" in a:
            return "snowy.jpeg"
        else:
            return "moon.jpeg"
def putWeatherOnScreen():
    a = getWeather()


    images = []
    labels = []
    start_pos = 700
    for b in a[0:6]:

        for c in b:
            if "a" not in str(c):
                if "y" not in str(c):
                    if ":" not in str(c):
                        Label(text=str(c), fg="white", bg="black",anchor = "n", font=("Helvetica Neue light", 20)).place(x = start_pos +10 + (a.index(b) * 70), y = 1 + (b.index(c) * 30))
                    else:
                        Label(text=str(c), fg="white", bg="black", anchor="n", font=("Helvetica Neue light", 20)).place(
                            x=start_pos + (a.index(b) * 70), y=1 + (b.index(c) * 30))
                else:


                    Label(image=get_thumbnails(c), width=60, bg="black", fg="white").place(x = start_pos+ (a.index(b) * 70), y = 1 + (b.index(c) * 30))
            else:

                Label(image=get_thumbnails(c), width=60, bg="black", fg="white").place(x = start_pos - 7+ (a.index(b) * 70), y = 1 + (b.index(c) * 30))
    return images
def addBtc():
    a = Label(text=str(getBtc()),anchor = "nw", fg="white",width = 50, bg="black", font=("Helvetica Neue light", 20))
    a .place(x = LEFT_SIDE, y = 1)
def convertFrom(a):
    c = a.index('<')
    return a[0:c]
def take_name(str):
    c = '"'
    a = [pos for pos, char in enumerate(str) if char == c]
    return str[1:a[1]]

def get_all_names(a):
    end_arr = []
    for x in range(0, 9, 2):
        end_arr.append(take_name(a[x]))

    return end_arr

def get_all_subjects(a):
    for x in range(1, 9, 2):
        print ((a[x]))
def addEmails():
   a = read_email_from_gmail()
def addNewsFeed():
    newsArr = getHeadlines(cnnUS)
    Label(text="News", fg="white", bg="black", font=("Helvetica Neue light", 40)).place(x = LEFT_SIDE, y = 100)
    for x in newsArr[0:8]:
        Label(text=str(x),bd = 2,relief = "flat", fg="white", bg="black",anchor = "nw", width=50, font=("Helvetica Neue light", 20)).place(x = LEFT_SIDE, y = 175 +(newsArr.index(x)*25) )

def tick():

    s = time.strftime('%I:%M')
    h = time.strftime("%I")
    if h != clock["text"].split(":")[0]:
        update()
    if s != clock["text"]:
        clock["text"] = s


    clock.after(200, tick)

def update():
    addBtc()
    addHashRate()
    addNewsFeed()
    images = putWeatherOnScreen()
    print "Updated"
    return images
root = Tk()
add_images_to_public()
root.configure(background = "black")
app = FullScreenApp(root)
clock = Label(root, fg="white", bg="black",anchor = "nw", font=("Helvetica Neue light", 80))
clock.place(x = 700, y = 100)


tick()
images = update()
root.mainloop()
