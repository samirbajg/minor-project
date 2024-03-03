import re
import requests
import string
import joblib
import numpy as np
import pandas as pd
import nltk
from nltk.stem import PorterStemmer
import flask
from flask import Flask, render_template, request
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from yt_comment_scrap import get_comments

pipe_nb = joblib.load(open("models/svm_classifier.pkl", "rb"))

def predict_emotions(text):
    return pipe_nb.predict([text])

nltk.download('wordnet')

ps = PorterStemmer()

stopwords=set(['br', 'the', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
                "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves',
                'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
                'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who',
                'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were',
                'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
                'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
                'at', 'by', 'for', 'with', 'about', 'between', 'into', 'through', 'during',
                'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
                'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
                'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only',
                'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
                'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
                'couldn', 'didn', 'doesn','hadn', 'hasn','haven','isn', 'ma', 'mightn', 'mustn',
                'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn'])

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]','',text)
    text = re.sub(r'\d+','',text)
    return text
def rem_wspaces(text):
    return ' '.join(text.split())
def rem_tags_urls(text):
    text = re.sub(r"http?://\S+|www.\.\S+", "", text)
    return re.sub(r'<.*?>','',text)
def tokenize(text):
    text = text.strip('.')
    return text.split()
def rem_stopwords(text):
    t_text = tokenize(text)
    f_text = [word for word in t_text if word not in stopwords]
    return f_text
def text_preprocess(text):
    #Remove puctuations, numbers and convert string into lower case
    text = clean_text(text)
    #Remove HTML tags and URLs
    text = rem_tags_urls(text)
    #Remove whitespaces
    text = rem_wspaces(text)
    #Tokenize the text
    text = rem_stopwords(text)
    return text
def stem_text(text):
    word_tokens = tokenize(text)
    return [ps.stem(words) for words in word_tokens]

def text_processing_pipeline(text):
    text = text_preprocess(text)
    text = ' '.join(text)
    text = stem_text(text)
    text = ' '.join(text)
    return text

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def create_app():
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/results',methods=['POST'])
    def result():
        url = request.form.get('url')
        try:
            url.raise_for_status()

            comments = get_comments(url)
            temp = []

            for comm in comments:
                temp.append(text_processing_pipeline(comm))

            clean_comments = temp


            labels = []
            ang,dis,fear,joy,neu,sad,love,sur = 0,0,0,0,0,0,0,0
            for i in clean_comments:
                emotion = predict_emotions(i)
                labels.append(emotion)

                if emotion == 'anger':
                    ang+=1
                elif emotion == 'fear':
                    fear=+1
                elif emotion == 'joy':
                    joy+=1
                elif emotion == 'love':
                    love+=1
                elif emotion == 'sadness':
                    sad+=1
                elif emotion == 'surprise':
                    sur+=1
                else:
                    neu+=1
            e_no = [ang,love,fear,joy,sad,sur]
            return render_template('result.html',n=len(clean_comments),ang=ang,love=love,fear=fear,joy=joy,sad=sad,sur=sur,e_no=e_no,comments=comments,labels=labels)
        except Exception as e:
            error_msg = f"Error: Invalid URL"
            return render_template('home.html',error_msg = error_msg)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
        
