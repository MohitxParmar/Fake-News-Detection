from flask import Flask, render_template, request, make_response, session, redirect, url_for
import pickle
import numpy as np
import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from functools import wraps
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)


conn = sqlite3.connect("signupDetails.db")
c= conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, email TEXT, password TEXT)")
conn.commit()
conn.close()

userId = 0

@app.route('/', methods = ["GET","POST"])
def man():
    msg = None
    if(request.method == "POST"):
        if(request.form["username"]!="" and request.form["password"]!=""):
            username = request.form["username"]
            emailId = request.form["email"]
            password = request.form["password"]
            conn = sqlite3.connect("signupDetails.db")
            c= conn.cursor()
            c.execute("INSERT INTO users VALUES('"+username+"','"+emailId+"','"+password+"')")
            conn.commit()
            conn.close()
            msg="Your account has been created !"
        else:
            msg = "Please fill all the entries"

    return render_template('sign_up.html',msg = msg)



@app.route('/predict', methods=['POST','GET'])
def home():
     #take input from the form of home.html
    inp = request.form['text_inp']

    # load the pickle file which containes LR Model
    # LR_model = pickle.load(open('LR_fake_news.pkl', 'rb'))

    # load the pickle file which containes DT Model
    # DT_model = pickle.load(open('DT_fake_news.pkl', 'rb'))

    #load the pickle file which containes pac Model
    pac_model = pickle.load(open('pac_fake_news.pkl', 'rb'))

    # load the pickle file which containes rfc Model
    # RFC_model = pickle.load(open('RFC_fake_news.pkl', 'rb'))

    #To classify news
    news_category_model = pickle.load(open(r'Category classifier\news_category_classifier.pkl', 'rb'))
    news_category = news_category_model.predict([inp])
    categories = ['business', 'entertainment', 'politics', 'sport', 'tech']
    news_category = categories[int(news_category)]
    print(news_category)

    #load the pickle file which containes string to float converter
    model_tfidf_vectorizer = pickle.load(open('fake_news_tfidf_vectorizer.pkl', 'rb'))

    #tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    #This is to convert that string to float
    inp_ser = pd.Series(data=inp)
    tfidf_inp_ser = model_tfidf_vectorizer.transform(inp_ser)

    #To store all predictions of various Algorithm
    all_ans = []

    #Answer of LR
    # LR_ans = LR_model.predict(tfidf_inp_ser)
    # all_ans.append(LR_ans)

    # # Answer of DT
    # DT_ans = DT_model.predict(tfidf_inp_ser)
    # all_ans.append(DT_ans)

    # Answer of pac
    pac_ans = pac_model.predict(tfidf_inp_ser)
    all_ans.append(pac_ans)

    # Answer of pac
    # RFC_ans = RFC_model.predict(tfidf_inp_ser)
    # all_ans.append(RFC_ans)

    for i in all_ans:
        if i == 1:
            print('Real')
        elif i == 0:
            print('Fake')




    ''' if ans == 'REAL':
        pred = 1
    else:
        pred = 0 '''

    return render_template('after.html', data = pac_ans, news_category = news_category)
    # else:
    #     return redirect('/index')


@app.route("/login", methods = ["GET","POST"])
def login():
    r =""
    msg2 = ""

    if(request.method == "POST"):
        if(request.form["username"]!="" and request.form["password"]!=""):
            username = request.form["username"]
            password = request.form["password"]
            conn = sqlite3.connect("signupDetails.db")
            c= conn.cursor()
            c.execute("SELECT * FROM users WHERE username ='"+username+"' and password ='"+password+"'")
            r = c.fetchall()
            for i in r:
                if(username == i[0] and password == i[2]):
                    session["logedin"] = True
                    session["username"] = username
                    session["user_id"]=r[0][0]
                    userId = r[0][0]
                    
                    # return redirect("index")
                    return redirect(url_for('index', uname=username))
            else:
                msg2= "Please enter a valid username and password"
      
            
    return render_template("login.html",msg = msg2)


@app.route("/index")
def index():
    if 'user_id' in session:
        return render_template("home.html",msg=request.args.get('uname'))
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/userDet')
def userDet():
    conn = sqlite3.connect("signupDetails.db")
    c= conn.cursor()
    c.execute("SELECT * FROM users")
    r = c.fetchall()
    for i in r:
        if session["user_id"] == r[0][0]:
            return render_template("userProfile.html",data = str(i))

    return render_template("userProfile.html")


@app.route('/aboutUs')
def aboutUs():
    
    return render_template("aboutUs.html")



if __name__ == "__main__":
    # app.secret_key = 'some secret key'
    app.run(debug = True)

