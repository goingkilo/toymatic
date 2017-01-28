
from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template

import json

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

@app.route("/3c")
def col3p():
    a = json.load( open( './json/toymatic_products.json'))
    b = [a[x:x+3] for x in xrange(0, len(a), 3)]
    return render_template('3colportfolio.html', prods = b)


@app.route("/homepagewo")
def homepage1():
    return render_template('homepage_wo_banner.html')

@app.route("/")
def testo():
    a = json.load( open( './json/toymatic_products.json'))
    b = [a[x:x+4] for x in xrange(0, len(a), 4)]
    print json.dumps(b,indent=4)
    cats = json.load( open( './json/toymatic_categories.json'))
    return render_template('test.html',categories=cats,products=b )

@app.route("/item")
def item():
    a = json.load( open( './json/toymatic_products.json'))
    b = [a[x:x+4] for x in xrange(0, len(a), 4)]
    return render_template("item.html", prods = b)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()
