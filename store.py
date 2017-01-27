from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template

import json

app = Flask(__name__)

@app.route("/paper")
def paper():
    return render_template('paper.html')


@app.route("/store")
def store():
    prods = json.load( open( './json/toymatic_products.json'))
    cats = json.load( open( './json/toymatic_categories.json'))
    return render_template('store.html',categories=cats,products=prods )

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/homepage")
def homepage():
    return render_template('homepage.html')

@app.route("/homepagewo")
def homepage1():
    return render_template('homepage_wo_banner.html')

@app.route("/t")
def testo():
    prods = json.load( open( './json/toymatic_products.json'))
    cats = json.load( open( './json/toymatic_categories.json'))
    return render_template('test.html',categories=cats,products=prods )

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()

