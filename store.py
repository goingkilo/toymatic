from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template

import json

app = Flask(__name__)

@app.route("/paper")
def index():
    return render_template('paper.html')


@app.route("/")
def store():
    prods = json.load( open( './json/toymatic_products.json'))
    cats = json.load( open( './json/toymatic_categories.json'))
    print json.dumps(prods, indent=4)
    return render_template('index.html',categories=cats,products=prods )


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()

