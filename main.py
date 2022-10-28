from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector
from bs4 import BeautifulSoup
from datetime import timedelta
import json
import requests
import lxml


#Flask app variables
app = application =  Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.permanent_session_lifetime = timedelta(days=7)

#Connection details
user='root'
password = 'Cloudproject##'
host = '34.134.204.196'
database = 'cloudproject'
#End connection details

conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS userdata (username VARCHAR(100) UNIQUE, email VARCHAR(200) UNIQUE, password VARCHAR(200))')
#headers
headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip', 
'DNT' : '1', # Do Not Track Request Header 
'Connection' : 'close'})

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
        cur.execute('select * from userdata where (username= "{}" or email= "{}") and password= "{}"'.format(uname, uname, passw))
        results = cur.fetchall()
        print(len(results))
        if len(results) == 0:
            flash("Please check the credentials and try again")
        else:
            for row in results:
                if (row[0] == "{}".format(uname) or row[1] == "{}".format(uname)) and row[2] == "{}".format(passw):
                    if remem == "on":
                        session.permanent = True
                        session['user'] = row[0]
                    else:
                        session['user'] = row[0]
                    return redirect(url_for('user'))
    else:
        if 'user' in session:
            return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'user' in session:
        user = session['user']
        return render_template('DashManager.html', user=user)
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
        cur.execute('INSERT INTO userdata (username, email, password) VALUES {}'.format(datatuple))
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
        cur.execute('INSERT INTO userdata (username, email, password) VALUES {}'.format(datatuple))
        conn.commit()
        cur.close()
        if 'user' in session:
            session.pop('user', None)
            return redirect(url_for('login'))
        else:
            return render_template('login.html')

@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    if 'user' in session:
        return render_template('userhome.html')
    else:
        return redirect(url_for('login'))

@app.route('/results', methods =['GET','POST'])
def getUserDetails():
    if 'user' in session:
        url = request.form.get('url')
        price_limit = request.form.get('price')
        date_range_from = request.form.get('date1')
        date_range_to = request.form.get('date2')
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

            print(title)
            print(price)
            print(image)
        return render_template('results.html', title=title,price=price,date_range_from=date_range_from,date_range_to=date_range_to, image=image)
    else:
        return redirect(url_for('login'))

print("ssdsss")

if __name__ == '__main__':
    app.run(debug=True)