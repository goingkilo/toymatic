from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template

from flask.ext.login import LoginManager
from flask.ext.login import login_required

import json

app = Flask(__name__)
login_manager = LoginManager(app)

@app.route("/map")
def root():
    return render_template('map.html')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()

