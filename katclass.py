from lib2to3.pgen2 import driver
from operator import truediv
from pydoc import classname
from time import sleep
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
import re
from sys import exit
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
import json
import uuid
from katowice import *
cnx = mysql.connector.connect(user='ikeaik', password='ikeaik',
                              host='51.75.53.71',
                              database='factory')
cursor = cnx.cursor()

timeout = 120

 
class Test1():
  
 def cenyupextra(self,ida):
 
  query = "SELECT * FROM accountallegro WHERE id=2"
  cursor.execute(query)
  get = cursor.fetchone()
  tokens = json.loads(get[6])
  access_token = tokens['access_token']
  ida = str(ida)

  ceny = "SELECT * FROM ikeamagazyn WHERE ida=" + ida
  cursor.execute(ceny)
  get = cursor.fetchone()
  pln = get[12]
 
 #if '/' in pln:
  #  pln = pln.split("/")[0]
 #if "Cena" in pln:
 #   pln = pln.split(" ")[1]
 #if ",-" in pln:
 #   pln = pln.replace(",-", ".00")
 #if "-" in pln:
 #   pln = pln.replace("-", ".00")
 #if pln.strip() == pln and " " not in pln:
 #   pln = pln.split()[0]
 #pln = pln.replace(",", ".")
  pln = float(pln)

  gg  = get[28]
  gg = float(gg)
 
  wikei = float(get[15])
  wikeikrk = float(get[19])
 
  base_amount = 100

  if pln <= 40:
     if gg > 2:
      marza = 45
     else:
      marza = 36     
  elif pln >= 41 and pln <= 79:
     marza = 36
  elif pln >= 80 and pln <= 150:
     marza = 36
  elif pln >= 151:
     marza = 36
  else:
     marza = 36
     
  try:
   #url = 'https://api.allegro.pl/sale/offers/'+ida
   #headers = {'Authorization': 'Bearer ' + access_token, 'Accept': "application/vnd.allegro.public.v1+json"}
   #response = requests.request("GET", url, headers=headers)
   #response_json = response.json()
   #cenauk = response_json["sellingMode"]["price"]["amount"]

   #uris = 'https://api.allegro.pl/pricing/offer-fee-preview'
   #headers = {'Accept': 'application/vnd.allegro.public.v1+json',
   #  'Authorization': 'Bearer ' + access_token}
   #dataa = {'offer': 'sdds'}
   #python_obj = {'offer': response_json}
   #myobj = json.dumps(python_obj)
   #response = requests.request("POST", uris, headers=headers , data=myobj)
 
   #response = response.json()
   #prowizja = response['commissions'][0]['fee']['amount']
   #prowizja = float(prowizja)
   #cenauk = float(cenauk)
   #prowizjaallegro = prowizja / cenauk * 100
   #prowizjaallegro = round(prowizjaallegro, 1)

  #pln = pln + (pln * (marza / 100)) + koszt + kurier + (pln * (prowizjaallegro / 100))
   pln = pln + (pln * marza / 100)

   if wikeikrk <= 5:
    pln = pln + 20 + marza * 50/100

   if wikei <= 20:
    pln = pln + 20 + pln + marza * 50/100

  
   suma = round(pln, 1)
   suma = str(suma)
   suma = suma.split('.')
   suma = suma[0] + '.89'
 
   suma = float(suma)

   if suma >= 38 and suma <= 39.99:
     suma = 40.00

   if suma >= 40 and suma <= 42:
     suma = 40.00

   pln = suma
   pln = '{:.2f}'.format(pln)
   print(pln)
  
   session = requests.Session()
   
   uri22 = f'https://api.allegro.pl/sale/product-offers/'+ida
   headers = {'Accept': 'application/vnd.allegro.public.v1+json',
     'Authorization': 'Bearer ' + access_token,
     'Content-Type': 'application/vnd.allegro.public.v1+json'
     }
   datawww = {"sellingMode":{"price":{"amount": pln,"currency": "PLN"}}}
   myobjw = json.dumps(datawww)
   response = session.request("PATCH", uri22, headers=headers , data=myobjw)
   #print(response.json())
   response_dict = response.json()
   response_text = json.dumps(response_dict)
   response_dict = response.json()
   response_text = json.dumps(response_dict)
   #pprint(response_text)
   if "errors" in response_text:
     for error in response_dict['errors']:
      if 'Uzupełnij parametry obowiązkowe: EAN (GTIN).' in error['userMessage']  or ('Uzupełnij parametry obowiązkowe: EAN (GTIN).' in error['userMessage']):
       with open('aukcja.txt', 'a') as f:
        f.write(response_text + " " + id)
        f.write('\n')
  except Exception:
   response_dict = response.json()
   response_text = json.dumps(response_dict)

   with open('code.txt', 'a') as f:
    f.write(response_text + " extra")
    f.write('\n')  
 
 def user(self, name):

  cursor.execute("select * from `ikeamagazyn` WHERE name ='"+name+"'")
  myresult = cursor.fetchall()
  for row in myresult:
   userid = row[29]
   idaa = row[1]
   wykl = float(row[26])
   userid = float(userid)
   if wykl == 0:
    if userid == 2:
     self.cenyupextra(idaa)
    elif userid == 3:
     self.cenyupbest(idaa)
    elif userid == 5:
     return 
    else:
     print(userid)

 def verify(self, driver):
  if driver.find_element(by=By.CLASS_NAME, value='pip-product__buy-module-item-avaialability-group'):
    gg = driver.find_element(by=By.CLASS_NAME, value='pip-product__buy-module-item-avaialability-group').text
    if gg.find("Towar niedostępny w sklepach")!=-1:
     return True
    elif gg.find("Produkt nie jest sprzedawany w żadnym ze sklepów")!=-1:
     return True
    elif gg.find("Spróbuj ponownie")!=-1:
     return True
    elif gg.find("Brak w magazynie.")!=-1:
     return True  
    elif gg.find("Sprawdzamy dostępność")!=-1:
     return True
    elif gg.find("Produkt niedostępny")!=-1:
     return True
    elif gg.find("wyczerpany")!=-1:
     return True
    elif gg.find("tylko")!=-1:
     return True
    elif gg.find("Produkt nie jest dostępny")!=-1:
     return True  
    elif gg.find("Sprawdzanie dostepnosci...")!=-1:
     driver.refresh() 
    else:
     return False
  elif driver.find_element(by=By.CLASS_NAME, value='pip-stockcheck__item-link'):
    gg = driver.find_element(by=By.CLASS_NAME, value='js-stockcheck-section').text
    if gg.find("Towar niedostępny w sklepach")!=-1:
     return True
    elif gg.find("Produkt nie jest sprzedawany w żadnym ze sklepów")!=-1:
     return True
    elif gg.find("Brak w magazynie.")!=-1:
     return True 
    elif gg.find("Produkt nie jest dostępny")!=-1:
     return True      
    elif gg.find("Spróbuj ponownie")!=-1:
     return True
    elif gg.find("Sprawdzamy dostępność")!=-1:
     return True
    elif gg.find("wyczerpany")!=-1:
     return True
    elif gg.find("Produkt niedostępny")!=-1:
     return True
    elif gg.find("tylko")!=-1:
     return True
    elif gg.find("Sprawdzanie dostepnosci...")!=-1:
     driver.refresh() 
    else:
     return False 

 def dostawa():
    gg = driver.find_element(by=By.CLASS_NAME, value='pip-product__buy-module-item-avaialability-group').text	 
    #sleep(1)
    if gg.find("Obecnie ograniczone")!=-1:
     return True
    if gg.find("Obecnie niedostępne")!=-1:
     return True
    if gg.find("Obecnie niesprzedawane")!=-1:
     return True
    else:
     return False

 def family():
    try:
     driver.find_element(by=By.XPATH, value='//*[@id="pip-buy-module-content"]/div[2]/div[3]')
    except NoSuchElementException:
     return False
    return True

 def price(self, driver):
   pln = driver.find_element(by=By.CLASS_NAME, value='pip-temp-price-module__primary-currency-price').text
   #print(pln)
   if '/' in pln:
    pln = pln.split("/")[0]
   if "Cena" in pln:
    pln = pln.split(" ")[1]
   if ",-" in pln:
    pln = pln.replace(",-", ".00")
   if "-" in pln:
    pln = pln.replace("-", ".00")
   if pln.strip() == pln and " " not in pln:
    pln = pln.split()[0]
    
   pln = pln.replace(",", ".")
   
   return pln

 def closea(self,name):
  print("closea")
  s = requests.Session()
  cursor.execute("select * from `ikeamagazyn` where `name` = '"+name+"'")
  myresult = cursor.fetchall()
  for row in myresult:
   if int(row[15]) < 25 and int(row[19]) < 55:
       if row[26] == 0:
        
        cursor.execute("select * from `accountallegro` where `id` = "+ row[29] +" ")
        myresultt = cursor.fetchall()
        for rows in myresultt:
          tokens = json.loads(rows[6])
          access_token = tokens['access_token']
          #pprint(access_token)
          url = "https://api.allegro.pl/sale/offer-publication-commands/"+str(uuid.uuid1())
          payload = '{"publication": {"action": "END"},"offerCriteria": [{"offers":[{"id": "'+ row[1] +'"}],"type": "CONTAINS_OFFERS"}]}'
          headers = {'Authorization': 'Bearer ' + access_token, 'Accept': "application/vnd.allegro.public.v1+json"}
          response = s.request("PUT", url, headers=headers, data=payload)
          sql = "UPDATE ikeamagazyn SET `close` ='1'  WHERE name ='"+name+"'"
          cursor.execute(sql)
          cnx.commit() 
   else:
     return

 def closup(self,name):
  print("closup")
  s = requests.Session()
  cursor.execute("select * from `ikeamagazyn` where `name` = '"+name+"'")
  myresult = cursor.fetchall()
  for row in myresult:
   if int(row[26]) == 0:
     if row[15] > 26:
        cursor.execute("select * from `accountallegro` where `id` = "+ row[29] +" ")
        myresultt = cursor.fetchall()
        for rows in myresultt:
         tokens = json.loads(rows[6])
         access_token = tokens['access_token']
         #pprint(access_token)
         url = "https://api.allegro.pl/sale/offer-publication-commands/"+str(uuid.uuid1())
         payload = '{"publication": {"action": "ACTIVATE"},"offerCriteria": [{"offers":[{"id": "'+ row[1] +'"}],"type": "CONTAINS_OFFERS"}]}'
         headers = {'Authorization': 'Bearer ' + access_token, 'Accept': "application/vnd.allegro.public.v1+json"}
         response = s.request("PUT", url, headers=headers, data=payload)
         sql = "UPDATE ikeamagazyn SET `close` ='0'  WHERE name ='"+name+"'"
         cursor.execute(sql)
         cnx.commit() 
         #self.user(name)
     else:
      return
   else:
    return

 def cenyupbest(self, ida):
  cnx = mysql.connector.connect(user='ikeaik', password='ikeaik',
                              host='51.75.53.71',
                              database='factory')
  cursor = cnx.cursor()
 
  query = "SELECT * FROM accountallegro WHERE id=3"
  cursor.execute(query)
  get = cursor.fetchone()
  tokens = json.loads(get[6])
  access_token = tokens['access_token']


  id = str(ida)
 
  ceny = "SELECT * FROM ikeamagazyn WHERE ida=" + id
  cursor.execute(ceny)
  get = cursor.fetchone()
  pln = get[12]
 
 #if '/' in pln:
  #  pln = pln.split("/")[0]
 #if "Cena" in pln:
 #   pln = pln.split(" ")[1]
 #if ",-" in pln:
 #   pln = pln.replace(",-", ".00")
 #if "-" in pln:
 #   pln = pln.replace("-", ".00")
 #if pln.strip() == pln and " " not in pln:
 #   pln = pln.split()[0]
 #pln = pln.replace(",", ".")
  pln = float(pln)

  gg  = get[28]
  gg = float(gg)
 
  wikei = float(get[15])
  wikeikrk = float(get[19])
 
  base_amount = 100

  if pln <= 40:
     if gg > 2:
      marza = 45
     else:
      marza = 30     
  elif pln >= 41 and pln <= 79:
     marza = 30
  elif pln >= 80 and pln <= 150:
     marza = 30
  elif pln >= 151:
     marza = 30
  else:
     marza = 30
  try:
   #url = 'https://api.allegro.pl/sale/offers/'+id
   #headers = {'Authorization': 'Bearer ' + access_token, 'Accept': "application/vnd.allegro.public.v1+json"}
   #response = requests.request("GET", url, headers=headers)
   #response_json = response.json()
   #cenauk = response_json["sellingMode"]["price"]["amount"]

   #uris = 'https://api.allegro.pl/pricing/offer-fee-preview'
   #headers = {'Accept': 'application/vnd.allegro.public.v1+json',
   #  'Authorization': 'Bearer ' + access_token}
   #dataa = {'offer': 'sdds'}
   #python_obj = {'offer': response_json}
   #myobj = json.dumps(python_obj)
   #response = requests.request("POST", uris, headers=headers , data=myobj)
 
   #response = response.json()
   #prowizja = response['commissions'][0]['fee']['amount']
   #prowizja = float(prowizja)
   #cenauk = float(cenauk)
   #prowizjaallegro = prowizja / cenauk * 100
   #prowizjaallegro = round(prowizjaallegro, 1)

  #pln = pln + (pln * (marza / 100)) + koszt + kurier + (pln * (prowizjaallegro / 100))
   pln = pln + (pln * marza / 100)
 
   if wikeikrk <= 20:
     pln = pln + 20 + marza * 50/100

   if wikei <= 20:
     pln = pln + 20 + marza * 50/100

 
   suma = round(pln, 1)
   suma = str(suma)
   suma = suma.split('.')
   suma = suma[0] + '.79'
 
   suma = float(suma)

   if suma >= 38 and suma <= 39.99:
     suma = 40.10

   if suma >= 40 and suma <= 42:
     suma = 40.10
   s = requests.Session()

   pln = suma
   pln = '{:.2f}'.format(pln)
  #print(pln)
   uri22 = f'https://api.allegro.pl/sale/product-offers/'+id
   headers = {'Accept': 'application/vnd.allegro.public.v1+json',
     'Authorization': 'Bearer ' + access_token,
     'Content-Type': 'application/vnd.allegro.public.v1+json'
     }
   datawww = {"sellingMode":{"price":{"amount": pln,"currency": "PLN"}}}
   myobjw = json.dumps(datawww)
   response = s.request("PATCH", uri22, headers=headers , data=myobjw)
   #print(response.json())
   response_dict = response.json()
   response_text = json.dumps(response_dict)
   if "errors" in response_text:
     for error in response_dict['errors']:
      if 'Uzupełnij parametry obowiązkowe: EAN (GTIN).' in error['userMessage']  or ('Uzupełnij parametry obowiązkowe: EAN (GTIN).' in error['userMessage']):
       with open('aukcja.txt', 'a') as f:
        f.write(response_text + " " + id)
        f.write('\n')
   #print("zmiana best")
  except Exception:
   response_dict = response.json()
   response_text = json.dumps(response_dict)
   with open('code.txt', 'a') as f:
    f.write(response_text + " best")
    f.write('\n')

 def currentURL(self,curent, name):
  if curent == "https://www.ikea.com/pl/pl/cat/produkty-products/":
    self.closea(name)
    id = name
    chk = "5"
    szt= "0"
    upp = "0"
    uppk = "0"
    sql = "UPDATE ikeamagazyn SET wikeikrk ='"+ szt+ "', wikei ='"+szt+"', up ='"+upp+"', upk ='"+uppk+"', ikeacena ='100' ,  chk ='"+chk+"'  WHERE name ='"+id+"'"
    mycursor.execute(sql)
    cnx.commit()
    return False
  elif curent == "https://www.ikea.com/pl/pl/cat/produkty-products/#content":
    self.closea(name)
    id = name
    chk = "5"
    szt= "0"
    upp = "0"
    uppk = "0"
    sql = "UPDATE ikeamagazyn SET wikeikrk ='"+ szt+ "', wikei ='"+szt+"', up ='"+upp+"', upk ='"+uppk+"', ikeacena ='100' ,  chk ='"+chk+"'  WHERE name ='"+id+"'"
    mycursor.execute(sql)
    cnx.commit()
    return False
  else:
    return True 

 def gogo(self,name):
   #if odp:
    #   id = name
    #   chk = "5"
     #  szt= "0"
     #  upp = "1"
     #  uppk = "0"
     #  sql = "UPDATE ikeamagazyn SET wikei='0', up ='"+ upp+ "' WHERE name ='"+id+"'"
     #  cursor.execute(sql)
     #  cnx.commit()
     #  self.closea(name)
   #else:
       #bbC = self.price(driver)
       #numera = driver.find_element(By.CLASS_NAME, "pip-product-identifier__value").get_attribute("textContent")       
       #frame=driver.switch_to.active_element
       #element = WebDriverWait(driver, 20).until(
       #EC.presence_of_element_located((By.CLASS_NAME, "pip-stockcheck__item-link"))
       #)
       #element.click()
       #WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'pip-store-info__section')))
       #ilosc = frame.find_element(by=By.XPATH, value='//*[@id="range-modal-mount-node"]/div/div[3]/div/div[2]/div/div/div/div[1]/div[2]/span/span/strong[2]').text
       #digit = re.findall(r'\d+', ilosc) 
       #name = name
       #szt= ilosc
       #ikeapp = bbC
       #numer = numera
       #upp = "1"
       #pprint(numera)
       #sql = "UPDATE ikeamagazyn SET wikei ='"+ szt+ "' ,  ikeacena ='"+ikeapp+"' , numera ='"+ numera +"',  up ='"+upp+"'  WHERE name ='"+name+"'"
       #cursor.execute(sql)
       #cnx.commit()
       self.closup(name)
       self.closea(name)
       #pp = self.user(name)
       #pprint(pp)
 def setDriver(self, url, name, driver, ida):
  #driver.get(url)
  #test1 = Test1()
  #www = driver.current_url
  #sp = test1.currentURL(www, name)
  #if sp:
   # WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'pip-stockcheck__text-header-container')))  
    #bbC = test1.price(driver)
    #odp = test1.verify(driver)
    self.gogo(name)
     
#test = Test1()
#test.user("Pudełko IKEA GLIS 17 x 10 cm 3 SZTUKI")