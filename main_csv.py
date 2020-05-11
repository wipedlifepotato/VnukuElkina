#https://github.com/wipedlifepotato/VnukuElkina
#from config.config import config

from DonaPay.DonaPayMain import DonatePay
from config.config import config

import time
import subprocess # закинешь youtube-dl.exe... 
#import pafy # нет поддержки...
#https://console.developers.google.com/?pli=1 - govno ebanoje(нужно регистрировать API, не всегда удобно)
#import youtube_dl # нет полной поддержки...


import re


#pip3 install splinter requests urllib json re


class DonatePay_csv(DonatePay):
  def __init__(self):
   #self.videos=[]
   self.last_id=self.get_last_id()
   if self.last_id == False: self.last_id=0
  # ydl=youtube_dl.YoutubeDL()
   r = re.compile('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))')
   ids=[]
   while True:
    try:
       print("wait new videos")
       data_trans=self.getlasttrans()
       for i in data_trans:
        if i['id'] in ids: continue
        #print(i['comment'])
        ids.append(i['id'])
        urls=r.match(i['comment'])
        if urls is not None:
         urls=urls.groups()
         #print ( urls ) 
         title = subprocess.Popen(["youtube-dl", "--get-title","https://"+urls[2]],stdout=subprocess.PIPE).communicate()[0]
         duration = subprocess.Popen(["youtube-dl", "--get-duration","https://"+urls[2]],stdout=subprocess.PIPE).communicate()[0]

         video_title=str(title)
         video_duration=str(duration)
         sum_donation=str(i['sum']) 

         
         #video_title = json.loads(requests.get("https://noembed.com/embed?", params={"url" : "https://"+urls[2] }).content )['title']

         data={ 'title' : video_title, 'duration' : video_duration, 'payed' : sum_donation, 'minutes_payed': ((float(i['sum'])/config.price)), 'url':"https://"+urls[2]}
       
         print( data )
         self.update_csv( data )
         time.sleep(5)
         print("----")
         #TODO: собрать массив из этих видосов. и разобраться как лучше сортировать, и удалять то что посмотренно. 
       print("~~~ last id ~~~")
       
       self.last_id_update( data_trans )
       time.sleep(25)    
    except Exception as e:
     print ( "Exception: " + str(e) )
     time.sleep(25)
Don = DonatePay_csv()
  


