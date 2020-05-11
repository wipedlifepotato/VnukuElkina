from random import randint
#
class config:
 token="SkpHK9JacPYyKQRpjZgZ7d3natGwwjtWV0dg3RAhFeiuA5pcXOuqMcTbVvGO" #Тут свой ключ, елцин из https://donatepay.ru/page/api
 price=10 #стоимость минуты
 def getRandUserAgent(notNeed=True): # это не надо, мб пригодится
  
  user_agents = ""
  tmp = " "
  f=open('user_agents.txt')
  while tmp != "":
   user_agents = user_agents+f.read(2048)
  user_agents.split(';')
  return user_agents[randint(0,len(user_agents)-1)]

