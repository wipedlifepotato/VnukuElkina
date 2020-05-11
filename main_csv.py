#https://github.com/wipedlifepotato/VnukuElkina
from config.config import config
#from random import randint
import time
#from splinter import Browser #https://github.com/mozilla/geckodriver/releases/
import requests
import urllib
import json
import subprocess # закинешь youtube-dl.exe... 
#import pafy # нет поддержки...
#https://console.developers.google.com/?pli=1 - govno ebanoje
#import youtube_dl # нет полной поддержки...


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
   #print("last id %s" % i)
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
   self.videos=[]
  # ydl=youtube_dl.YoutubeDL()
   r = re.compile('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))')
   while True:
    
    try:
       print("wait new videos")
       data_trans=self.getlasttrans()
       for i in data_trans:
        #print(i['comment'])
        urls=r.match(i['comment'])
        if urls is not None:
         urls=urls.groups()
         #print ( urls )
         self.last_id_update( i['id'] ) 
         title = subprocess.Popen(["youtube-dl", "--get-title","https://"+urls[2]],stdout=subprocess.PIPE).communicate()[0]
         duration = subprocess.Popen(["youtube-dl", "--get-duration","https://"+urls[2]],stdout=subprocess.PIPE).communicate()[0]

         video_title=("Title:" +str(title))
         video_duration=("Duration:"+str(duration) )
         sum_donation=str(i['sum']) 

         
         #video_title = json.loads(requests.get("https://noembed.com/embed?", params={"url" : "https://"+urls[2] }).content )['title']
         print("Титл %s | время %s | Оплачено %s | минут проплачено %d | адрес(url) %s" % (video_title, video_duration, sum_donation, ((float(i['sum'])/config.price)), "https://"+urls[2]) )
         #time.sleep(30)
         print("----")
         #TODO: собрать массив из этих видосов. и разобраться как лучше сортировать, и удалять то что посмотренно. 
       time.sleep(25)    
    except Exception as e:
     
     print ( str(e) )
Don = DonatePlay()
  


