# -*- coding: utf-8 -*-
from Tkinter import *
from exchanges.bitfinex import Bitfinex
from bs4 import BeautifulSoup
import urllib2
import forecastio
import time
from PIL import ImageTk, Image,ImageFont, ImageDraw
import feedparser
import json
import random


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

import smtplib
import time
import imaplib
import email
t_c = "turquoise1"
list_of_Labels = []
public_images = []
greetings = ["Good to see you again", "Hello", "Looking good", "Hi", "Nice to see you", "Looking good!"]
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

cnnUS = "http://rss.cnn.com/rss/cnn_us.rss"
cnntech = "http://rss.cnn.com/rss/cnn_tech.rss"
slushUrl = "https://slushpool.com/accounts/profile/json/1787598-f474765ec374ff7e6ea8695635f1415f"
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
    d =Label(text=("Hashrate: " + str(hr)+ " Th/s"),bd = 2, fg = "white", bg = "black",anchor = "nw", width = 50, font = ("Helvetica Neue light", 15))
    d.place(x= LEFT_SIDE, y = 31)
    m =Label(text=("Reward: $" + str(r)),bd = 2, fg="white", bg="black",anchor = "nw", width=50, font=("Helvetica Neue light", 15))
    m.place(x= LEFT_SIDE, y = 61)
    list_of_Labels.append(d)
    list_of_Labels.append(m)
def convertTime(a):
    b = a + 4
    print b
    if b > 12:
        print "converting..."
        b %= 12
    print str(b) + ":00"
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
    size = 60, 60
    start_pos = 600

    for b in a[0:6]:

        for c in b:
            if "a" not in str(c):
                if "y" not in str(c):
                    if ":" not in str(c):
                        m = Label(text=str(c), fg="white", bg="black",anchor = "n", font=("Helvetica Neue light", 20))
                        m.place(x = start_pos +10 + (a.index(b) * 70), y = 1 + (b.index(c) * 30))
                        list_of_Labels.append(m)
                    else:
                        m = Label(text=str(c), fg="white", bg="black", anchor="n", font=("Helvetica Neue light", 20))
                        m.place(x=start_pos + (a.index(b) * 70), y=1 + (b.index(c) * 30))
                        list_of_Labels.append(m)
                else:



                    m = Label(image=get_thumbnails(c), width=60, bg="black", fg="white")
                    m.place(x = start_pos+ (a.index(b) * 70), y = 1 + (b.index(c) * 30))
                    list_of_Labels.append(m)
            else:

                m = Label(image=get_thumbnails(c), width=60, bg="black", fg="white")
                m.place(x = start_pos - 7+ (a.index(b) * 70), y = 1 + (b.index(c) * 30))
                list_of_Labels.append(m)
def addBtc():
    a = Label(text=str(getBtc()),anchor = "nw", fg="white",width = 50, bg="black", font=("Helvetica Neue light", 20))
    a .place(x = LEFT_SIDE, y = 1)
    list_of_Labels.append(a)
def convertFrom(a):
    c = a.index('<')
    return a[0:c]
def addEmails():
    a = read_email_from_gmail()
    for x in range (0, a.__len__(),2):
        Label(text=str(convertFrom(a[x])), bd=2, relief="flat", fg="white", bg="black", anchor="nw", width=50, font=("Helvetica Neue light", 20)).grid(column = 7, row = x + 4)
def addNewsFeed():
    newsArr = getHeadlines(cnnUS)
    d = Label(text="News", fg="white", bg="black", font=("Helvetica Neue light", 40))
    d.place(x = LEFT_SIDE, y = 100)
    list_of_Labels.append(d)
    for x in newsArr[0:8]:
       m = Label(text=str(x),bd = 2,relief = "flat", fg="white", bg="black",anchor = "nw", width=50, font=("Helvetica Neue light", 20))
       m.place(x = LEFT_SIDE, y = 175 +(newsArr.index(x)*30) )
       list_of_Labels.append(m)

def genRandomGreeting():
    random.shuffle(greetings)
    print greetings[0]
    return greetings[0]

def greet():
    s = ""
    for l in genRandomGreeting():
        s += l
        greeting["text"] = s
        time.sleep(.5)


def clearGreeting():
    greeting["text"] = ""

def destroyAll():
    for label in list_of_Labels:
        print label
        label.destroy()
def tick():

    s = time.strftime('%I:%M')
    h = time.strftime("%I")
    if h != clock["text"].split(":")[0]:
        update()
    if s != clock["text"]:
        clock["text"] = s

    clock.after(200, tick)

def update():
    destroyAll()
    addBtc()
    addHashRate()
    addNewsFeed()
    putWeatherOnScreen()
    print "Updated"

root = Tk()
add_images_to_public()
root.configure(background = "black")
addBtc()
addHashRate()
addNewsFeed()
putWeatherOnScreen()
app = FullScreenApp(root)
clock = Label(root, fg="white", bg="black",anchor = "nw", font=("Helvetica Neue light", 80))
clock.place(x = 700, y = 100)
greeting = Label(root, fg="white", bg="black",anchor = "nw", font=("Helvetica Neue light", 80))
greeting.place(x = 0, y = 500)
tick()
root.mainloop()


