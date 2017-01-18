from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template

from flask.ext.login import LoginManager
from flask.ext.login import login_required

import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/store")
def store():
    prods = json.load( open( './json/toymatic_products.json'))
    cats = json.load( open( './json/toymatic_categories.json'))
    print json.dumps(prods, indent=4)
    return render_template('store.html',categories=cats,products=prods )


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()

