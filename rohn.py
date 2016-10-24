# -*- coding: utf-8 -*-

from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template

from flask.ext.login import LoginManager
from flask.ext.login import login_required

from jinja2 import Environment, PackageLoader

import json

app = Flask(__name__)
login_manager = LoginManager(app)


import pagehelper
pages = pagehelper.getpages()

@app.route("/rohn")
def rohn():
    page_num = request.args.get("page")
    print page_num
    page_num = int(page_num)
    page1 =  pages[ page_num % len(pages)]
    pagenums = len(pages)
    return render_template( 'srohn.html', page = page1, numpages=pagenums)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()

