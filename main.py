#https://github.com/wipedlifepotato/VnukuElkina
from DonaPay.DonaPayMain import DonatePay
from config.config import config

from random import randint
import time
from splinter import Browser #https://github.com/mozilla/geckodriver/releases/
import requests
import urllib
import json

import re


#pip3 install splinter requests urllib json re

class DonatePlay_splinter(DonatePay):
  def __init__(self):
   self.last_id=self.get_last_id() #super(...)?
   if self.last_id == False: self.last_id=0
   r = re.compile('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))')
   try:
    # print("Start browser")
     with Browser() as brows: #user_agent=config.getRandUserAgent()) as brows:
      while True:
       print("wait new videos")
       data_trans=self.getlasttrans()
       self.last_id_update( data_trans )
       for i in data_trans:
        print(i['comment'])
        urls=r.match(i['comment'])
        if urls is not None:
         urls=urls.groups()
         print ( urls )
         print("Visiting")
         brows.visit( "https://"+urls[2] )#можно embed тот присобачить...
         time.sleep( 30+((float(i['sum'])/config.price)*60) ) #30 секунд на включение видео там... выключишь, если не нужно.
       
       time.sleep(25)
   except Exception as e:
    print ( str(e) )
Don = DonatePlay_splinter()
  


