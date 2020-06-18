# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 12:05:25 2020

@author: TrueCactus
"""
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='templates',static_folder='static')
model2=pickle.load(open('resultsKNN.sav','rb'))
XCOPY=pd.read_csv('XCOPY.csv')


def ImageDeFilm (url) :
    pageA = requests.get(url)
    soup =  BeautifulSoup(pageA.content, 'html.parser')
    urlImage=soup.find(class_="poster").find("img").attrs['src']
    return urlImage


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mesrecommandationsdefilms',methods=['POST'])
def predict():

    int_features = [x for x in request.form.values()]
    final_features = int_features[0]
    IndexFilms=model2.kneighbors(XCOPY[[ 'Action', 'Adventure', 'Animation',
                            'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
                            'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical',
                            'Mystery', 'News', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War',
                            'Western'
                            ]][XCOPY["movie_title"].str.lower()==final_features.lower()])[1][0]
                          
                          
    ListeFilms=XCOPY['movie_title'].iloc[IndexFilms].values.tolist()

    output = ListeFilms
    film1=output[0]
    url1=ImageDeFilm (XCOPY['movie_imdb_link'][XCOPY["movie_title"].str.lower()==film1.lower()].values[0])
    film2=output[1]
    url2=ImageDeFilm (XCOPY['movie_imdb_link'][XCOPY["movie_title"].str.lower()==film2.lower()].values[0])
    film3=output[2]
    url3=ImageDeFilm (XCOPY['movie_imdb_link'][XCOPY["movie_title"].str.lower()==film3.lower()].values[0])
    film4=output[3]
    url4=ImageDeFilm (XCOPY['movie_imdb_link'][XCOPY["movie_title"].str.lower()==film4.lower()].values[0])
    film5=output[4]
    url5=ImageDeFilm (XCOPY['movie_imdb_link'][XCOPY["movie_title"].str.lower()==film5.lower()].values[0])
    return render_template('index.html', film1=film1,film2=film2,film3=film3,film4=film4,film5=film5, url1=url1,url2=url2,url3=url3,url4=url4,url5=url5)


if __name__ == "__main__":
    app.run()
