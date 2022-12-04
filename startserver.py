import mysql.connector
from bs4 import BeautifulSoup
import requests
import time
import random 

list1 = ["$50","$40","$30","$20","$10","$1"]

#Connection details
user='root'
password = 'Cloudproject##'
host = '34.134.204.196'
database = 'cloudproject'
#End connection details

conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
cur = conn.cursor()

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip', 
'DNT' : '1', # Do Not Track Request Header 
'Connection' : 'close'})

while True:
    cur = conn.cursor()
    cur.execute('SELECT currprice, link, desiredprice, UserID from productinfo')
    linklist = cur.fetchall()
    print(len(linklist))
    for data in linklist:
        response = requests.get(data[1], headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        newprice = random.choice(list1)#soup.find("span", attrs={'class':'a-offscreen'}).get_text()
        print(newprice)
        cur.execute("UPDATE productinfo SET currprice = '{}' where link = '{}' and UserID = '{}'".format(newprice, data[1], data[3]))
        conn.commit()
        cur.close()
    time.sleep(30)