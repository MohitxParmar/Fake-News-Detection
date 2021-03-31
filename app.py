from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


app = Flask(__name__)

@app.route('/')
def man():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def home():
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

if __name__ == "__main__":
    app.run(debug = True)

