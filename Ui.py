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
    Label(text=("Hashrate: " + str(hr)+ " Th/s"),bd = 2, fg = "white", bg = "black",anchor = "nw", width = 50, font = ("Helvetica Neue light", 20)).grid(row=1,column=0)
    Label(text=("Reward: $" + str(r)),bd = 2, fg="white", bg="black",anchor = "nw", width=50, font=("Helvetica Neue light", 20)).grid(row= 2, column=0)
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
    if "Cloudy" in a:
        return 'cloudy.jpeg'
    elif "Rain" in a:
        return 'rainy.jpeg'
    elif "Sunny" in a:
        return "sunny.jpeg"
    else:
        return "sunny.jpeg"
def putWeatherOnScreen():
    a = getWeather()
    size = 60, 60
    images = []
    for b in a[0:6]:

        for c in b:
            if "a" not in str(c):
                if "y" not in str(c):
                    Label(text=str(c), fg="white", bg="black", font=("Helvetica Neue light", 20)).grid(row=b.index(c),
                                                                                                       column=a.index(
                                                                                                           b) + 2)
                else:

                    ab = Image.open(getImage(c))
                    ab.thumbnail(size, Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(ab)
                    images.append(photo)

                    Label(image=photo, width=60, bg="black", fg="white").grid(row=b.index(c), column=a.index(b) + 2)
            else:

                ab = Image.open(getImage(c))
                ab.thumbnail(size, Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(ab)
                images.append(photo)

                Label(image=photo, width=60, bg="black", fg="white").grid(row=b.index(c), column=a.index(b) + 2)
    return images
def addBtc():
    Label(text=str(getBtc()),anchor = "nw", fg="white",width = 50, bg="black", font=("Helvetica Neue light", 20)).grid(row=0, column=0)
def convertFrom(a):
    c = a.index('<')
    return a[0:c]
def addEmails():
    a = read_email_from_gmail()
    for x in range (0, a.__len__(),2):
        Label(text=str(convertFrom(a[x])), bd=2, relief="flat", fg="white", bg="black", anchor="nw", width=50, font=("Helvetica Neue light", 20)).grid(column = 7, row = x + 4)
def addNewsFeed():
    newsArr = getHeadlines(cnnUS)
    Label(text="   ", fg="white", bg="black", width=30,height = 3, font=("Helvetica Neue light", 30)).grid(row=5, column=0)
    Label(text="News", fg="white", bg="black", width=30, font=("Helvetica Neue light", 40)).grid(row=6, column=0)
    for x in newsArr[0:8]:
        Label(text=str(x),bd = 2,relief = "flat", fg="white", bg="black",anchor = "nw", width=50, font=("Helvetica Neue light", 20)).grid(row=newsArr.index(x) + 7, column=0)
def tick():
    s = time.strftime('%I:%M')
    if s != clock["text"]:
        clock["text"] = s
    clock.after(200, tick)
root = Tk()
root.configure(background = "black")
addBtc()
addHashRate()
addNewsFeed()
images = putWeatherOnScreen()
app = FullScreenApp(root)
clock = Label(root, fg="white", bg="black",anchor = "nw", font=("Helvetica Neue light", 80))
clock.grid(row=0, column=8)


tick()

root.mainloop()