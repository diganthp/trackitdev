import mysql.connector
import random
import lxml
import requests
from bs4 import BeautifulSoup
import time
import smtplib

list1 = ["$50","$40","$30","$20","$10","$1"]
#Connection details
user='root'
password = 'Group31sql@@'
host = '34.173.118.13'
database = 'group31db'
#End connection details

conn = mysql.connector.connect(user=user, password=password, host=host, database=database)

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip', 
'DNT' : '1', # Do Not Track Request Header 
'Connection' : 'close'})


def sendemail():
    password = "phgnaqjbcjdjmayh"
    
    return None

def checkamazon():
    while True:
        cur = conn.cursor()
        cur.execute('SELECT currprice, link, desiredprice, UserID from productinfo')
        linklist = cur.fetchall()
        print(linklist)
        print(len(linklist))
        for data in linklist:
            response = requests.get(data[1], headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')
            newprice = random.choice(list1) #soup.find("span", attrs={'class':'a-offscreen'}).get_text()
            print(newprice)
            cur = conn.cursor()
            cur.execute("UPDATE productinfo SET currprice = '{}' where link = '{}' and UserID = '{}'".format(newprice, data[1], data[3]))
            conn.commit()
            cur.execute("select * from productinfo")
            justlist = cur.fetchall()
            print(justlist)
            cur.close()
            time.sleep(5)
            desireprice = data[2]
            if newprice <= desireprice:
                sendemail()
        time.sleep(120)

checkamazon()