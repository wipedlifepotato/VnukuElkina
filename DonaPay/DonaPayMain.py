from config.config import config
import requests
import urllib
import json
import os.path
import csv

class DonatePay():
  def last_id_update(self,trans):
   min = self.last_id
   for i in trans:
    if i['id'] > min: min=i['id']
   if min != self.last_id: self.last_id=min
   f=open('last_id', "w")
   print("write to last id: %d" % self.last_id) 
   f.write( str(self.last_id) )
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
   print("payload: ")
   print ( payload )
   r= requests.get(addr,params=payload)
   return json.loads(r.content)
  def update_csv(self, data):
   exists=os.path.isfile('Videos.csv') 
   f=open('Videos.csv', 'a', encoding='utf-8')
   #Титл, ссылка, оплачено, длительность видео, оплачено минут.
   fnames = ['title', 'url', 'payed', 'duration', 'minutes_payed']
   writer = csv.DictWriter(f,fieldnames=fnames, delimiter="|")
   if not exists:
    writer.writeheader()

   writer.writerow(data)
   f.close()
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
