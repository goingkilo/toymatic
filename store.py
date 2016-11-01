from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template

from flask.ext.login import LoginManager
from flask.ext.login import login_required

import json


app = Flask(__name__)

# login_manager = LoginManager(app)
# login_manager.init_app(app)


import pagehelper
pages = pagehelper.getpages()

@app.route("/rohn")
def rohn():
    page_num = request.args.get("page")
    print page_num
    page_num = int(page_num)
    page1 =  pages[ page_num % len(pages)]
    page1 = page1.split('\n')
    pagenums = len(pages)
    print len(page1)
    return render_template( 'srohn.html', page = page1, numpages=pagenums, selectedpage=page_num)

@app.route("/store")
def store():
    import fk
    prods = fk.load_products('home_improvement_tools_')
    c = fk.load_categories()
    return render_template('store.html',categories=c,products=prods )

@app.route("/map")
def map():
    return render_template('map.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print 'logged in' ,request.form['email'] or 'None supplied' ,request.form['password'] or 'None supplied'
        return render_template('store.html')
    else:
        return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()

