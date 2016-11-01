# -*- coding: utf-8 -*-

from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template

from flask.ext.login import LoginManager
from flask.ext.login import login_required

from jinja2 import Environment, PackageLoader

import json

app = Flask(__name__)
login_manager = LoginManager(app)



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()

