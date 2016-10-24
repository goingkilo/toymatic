from flask import Flask,session, redirect, url_for, escape, request
from flask import render_template

from flask.ext.login import LoginManager
from flask.ext.login import login_required

#import fk
import json

app = Flask(__name__)
login_manager = LoginManager(app)

@app.route("/p/<product>")
def prods(product):
    c = None
    if session.has_key('cats'):
        c = session['cats']
    print product , c[product]
    if not c:
        c = fk.cat_local()
        session['cats']  = c
    a = fk.prod_local( product, session['cats'][product] )
    return render_template("inventory.html",products=a)

@app.route("/p.json/<product>")
def prod1s(product):
    c = None
    if session.has_key('cats'):
        c = session['cats']
    print product , c[product]
    if not c:
        c = fk.cat_local()
        session['cats']  = c
    a = fk.prod_local( product, session['cats'][product] )
    #return a
    return fk.parse_product( a)

@app.route("/c")
def cats():
    a = fk.cat_local()
    session['cats'] = a
    return render_template("cats.html",categories=a)


@app.route("/hello")
def hello():
    return render_template("index.html",variable="hello kitty!")

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()

