#https://github.com/wipedlifepotato/VnukuElkina
from config.config import config
from random import randint
import time
from splinter import Browser #https://github.com/mozilla/geckodriver/releases/
import requests
import urllib
import json

import re


#pip3 install splinter requests urllib json re

class DonatePlay():
  def last_id_update(self,_id):
   f=open('last_id', "w")
   print("write to last id: %d" % _id) 
   f.write( str(_id) )
   f.close()
  def get_last_id(self):
   try:
    f=open('last_id', "rb")
    i=f.read()
    if len(i) == 0: return False
    f.close()
    return int(i)
   except IOError:
    return False

    
   

  def get(self, addr, app_payload={}):
   payload = {'access_token': config.token, 'type': 'donation'} 
   payload.update( app_payload )
   r= requests.get(addr,params=payload)
   return json.loads(r.content)

  def getlasttrans(self, app_payload={}):
   
   i=self.get_last_id()
   print("last id %s" % i)
   if i != False:
    app_payload.update({"after":i})
   l=self.get( "https://donatepay.ru/api/v1/transactions?",app_payload )
   #print("new dontations %s" % l['count'])
   return l['data']


  def user(self):
   lasts=self.get( "https://donatepay.ru/api/v1/user?" )

  def send_notify(self, name, summ, comment): #test notify
   lasts=self.get( "https://donatepay.ru/api/v1/notification?", {'name':name,"sum":summ,"comment":comment} )

   print(lasts.content)

  def __init__(self):
   r = re.compile('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))')
   try:
    # print("Start browser")
     while True:
       print("wait new videos")
       data_trans=self.getlasttrans()
       for i in data_trans:
        print(i['comment'])
        urls=r.match(i['comment'])
        if urls is not None:
         urls=urls.groups()
         print ( urls )
         print("Visiting")
         self.last_id_update( i['id'] )
         with Browser() as brows: #user_agent=config.getRandUserAgent()) as brows:
          brows.visit( "https://"+urls[2] )#можно embed тот присобачить...
          #time.sleep(30)
          print( " sleep  %d seconds" % 30+((float(i['sum'])/config.price)*60)) 
          time.sleep( 30+((float(i['sum'])/config.price)*60) ) #30 секунд на включение видео там... выключишь, если не нужно.
       time.sleep(25)
   except Exception(e):
    print ( str(e) )
Don = DonatePlay()
  


