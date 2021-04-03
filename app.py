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
            msg="Your account is created"
        else:
            msg = "Please fill all the entries"

    return render_template('sign_up.html',msg = msg)



@app.route('/predict', methods=['POST','GET'])
def home():
    if 'user_id' in session:
        #take input from the form of home.html
        inp = request.form['text_inp']

        #load the pickle file which containes main ML Model
        model = pickle.load(open('fake_news.pkl', 'rb'))

        #load the pickle file which containes string to float converter
        model_tfidf_vectorizer = pickle.load(open('fake_news_tfidf_vectorizer.pkl', 'rb'))

        #tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        #This is to convert that string to float
        inp_ser = pd.Series(data=inp)
        tfidf_inp_ser = model_tfidf_vectorizer.transform(inp_ser)


        ans = model.predict(tfidf_inp_ser)
        if ans == 'REAL':
            pred = 1
        else:
            pred = 0

        return render_template('after.html', data = pred)
    else:
        return redirect('/')


@app.route("/login", methods = ["GET","POST"])
def login():
    r =""
    msg = ""

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
                    return redirect("index")
                else:
                    msg= "Please enter valid username and password"
      
            
    return render_template("login.html",msg = msg)


@app.route("/index")
def index():
    if 'user_id' in session:
        return render_template("home.html")
    else:
        return redirect('/')

# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__ == "__main__":
    # app.secret_key = 'some secret key'
    app.run(debug = True)

