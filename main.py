from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector
from bs4 import BeautifulSoup
from datetime import timedelta
import json
import requests
import lxml
import time
import random
from concurrent.futures import ThreadPoolExecutor

list1 = ["$50","$40","$30","$20","$10","$1"]
#Connection details
user='root'
password = 'Cloudproject##'
host = '34.134.204.196'
database = 'cloudproject'
#End connection details

conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
cur = conn.cursor()
#cur.execute('Truncate table productinfo')
cur.execute('CREATE TABLE IF NOT EXISTS userinfo (UserID INT UNIQUE AUTO_INCREMENT NOT NULL, username VARCHAR(100) UNIQUE, email VARCHAR(200) UNIQUE, password VARCHAR(200))')
cur.execute('CREATE TABLE IF NOT EXISTS productinfo (UserID INT NOT NULL, productname VARCHAR(1000), currprice VARCHAR(200), desiredprice VARCHAR(200), link VARCHAR(1000), image VARCHAR(1000))')
#headers
headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip', 
'DNT' : '1', # Do Not Track Request Header 
'Connection' : 'close'})

def sendemail():
    print("yay!!!!")
    return None

def checkamazon():
    while True:
        cur = conn.cursor()
        cur.execute('SELECT currprice, link, desiredprice, UserID from productinfo')
        linklist = cur.fetchall()
        print(len(linklist))
        for data in linklist:
            response = requests.get(data[1], headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')
            newprice = random.choice(list1) #soup.find("span", attrs={'class':'a-offscreen'}).get_text()
            print(newprice)
            cur.execute("UPDATE productinfo SET currprice = '{}' where link = '{}' and UserID = '{}'".format(newprice, data[1], data[3]))
            conn.commit()
            cur.close()
            desireprice = data[2]
            if newprice <= desireprice:
                sendemail()
        time.sleep(30)
#Flask app variables

app = application =  Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.permanent_session_lifetime = timedelta(days=7)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cur = conn.cursor()
        session.permanent = False
        uname = request.form.get('loginame')
        passw = request.form.get('loginpass')
        remem = request.form.get('meme')
        print("name: {}".format(uname))
        print("password: {}".format(passw))
        cur.execute('select * from userinfo where (username= "{}" or email= "{}") and password= "{}"'.format(uname, uname, passw))
        results = cur.fetchall()
        print(len(results))
        if len(results) == 0:
            flash("Please check the credentials and try again")
        else:
            for row in results:
                if (row[1] == "{}".format(uname) or row[2] == "{}".format(uname)) and row[3] == "{}".format(passw):
                    if remem == "on":
                        session.permanent = True
                        session['user'] = row[1]
                        session['user_id'] = row[0]
                    else:
                        session['user'] = row[1]
                        session['user_id'] = row[0]
                    return redirect(url_for('user'))
    else:
        if 'user' in session:
            return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'user' in session:
        user = session['user']
        cur = conn.cursor()
        cur.execute('SELECT * from productinfo where UserID ={}'.format(session['user_id']))
        prodlist = cur.fetchall()
        print(prodlist)        
        return render_template('dashboard.html', user=user, prodlist=prodlist)
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def signup():
    return render_template('register.html')

@app.route('/registerationaction', methods=['GET', 'POST'])
def registerationaction():
    if conn.is_connected() != True:
        conn.reconnect()
        cur = conn.cursor()
        signname = request.form.get('signupname')
        signmail = request.form.get('signupemail')
        signpassw = request.form.get('signuppass')
        datatuple = ("{}".format(signname), "{}".format(signmail), "{}".format(signpassw))
        cur.execute('INSERT INTO userinfo (username, email, password) VALUES {}'.format(datatuple))
        conn.commit()
        cur.close()
        if 'user' in session:
            session.pop('user', None)
            return redirect(url_for('login'))
        else:
            return render_template('login.html')
    else:
        cur = conn.cursor()
        signname = request.form.get('signupname')
        signmail = request.form.get('signupemail')
        signpassw = request.form.get('signuppass')
        datatuple = ("{}".format(signname), "{}".format(signmail), "{}".format(signpassw))
        cur.execute('INSERT INTO userinfo (username, email, password) VALUES {}'.format(datatuple))
        conn.commit()
        cur.close()
        if 'user' in session:
            session.pop('user', None)
            return redirect(url_for('login'))
        else:
            return render_template('login.html')

@app.route('/trackit', methods=['GET', 'POST'])
def userhome():
    if 'user' in session:
        user = session['user']
        return render_template('trackit.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/results', methods =['GET','POST'])
def results():
    if 'user' in session:
        user = session['user']
        url = request.form.get('proddurl')
        desprice = request.form.get('desprice')
        if request.method == "POST":            
            print(url)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')
            title = soup.find("span", attrs={"id":'productTitle'}).get_text().strip()
            price = soup.find("span", attrs={'class':'a-offscreen'}).get_text()

            img_div = soup.find(id="imgTagWrapperId")

            imgs_str = img_div.img.get('data-a-dynamic-image')  # a string in Json format
        
            imgs_dict = json.loads(imgs_str)    
            num_element = 0 
            image = list(imgs_dict.keys())[num_element]

            proddatatuple = ("{}".format(session['user_id']), "{}".format(title), "{}".format(price), "{}".format(desprice), "{}".format(url), "{}".format(image))
            cur = conn.cursor()
            cur.execute('INSERT INTO productinfo (UserID, productname, currprice, desiredprice, link, image) VALUES {}'.format(proddatatuple))
            conn.commit()
            cur.execute("SELECT * from productinfo where UserID ='{}'".format(session['user_id']))
            prodlist = cur.fetchall()
            cur.close()
        return render_template('dashboard.html', user=user, prodlist=prodlist)
    else:
        return redirect(url_for('login'))
    
@app.route('/graphs', methods=['GET','POST'])
def graphdata():
    prices = []
    dates = []
    temp1 = []
    temp2 = []
    cur.execute('SELECT Price FROM graphInformation')
    temp1 = cur.fetchall()
    for data in temp1:
        for item in data:
            prices.append(item)
    cur.execute('SELECT QueryTime FROM graphInformation')
    temp2 = cur.fetchall()
    for data in temp2:
        for item in data:
            dates.append(item)
    plt.bar(dates,prices)
    #plt.show()
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    return render_template("graphs.html",file =files)


print("ssdss")

if __name__ == '__main__':
    executor  = ThreadPoolExecutor(max_workers=1)
    executor.submit(checkamazon)
    app.run(debug=True)
