from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector
from bs4 import BeautifulSoup
from datetime import timedelta


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
headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

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
        print(results)
        for row in results:
            if (row[0] == "{}".format(uname) or row[1] == "{}".format(uname)) and row[2] == "{}".format(passw):
                print(row[0], row[1], row[2])
                if remem == "on":
                    session.permanent = True
                    session['user'] = uname
                else:
                    session['user'] = uname
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

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

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

print("ssdsssd")

if __name__ == '__main__':
    app.run(debug=True)