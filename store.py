
from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template
from flask_session import Session

import json,os


app = Flask(__name__)

@app.route("/paper")
def paper():
    return render_template('paper.html')

@app.route("/")
def col3p():
    a = json.load( open( './json/toymatic_products.json'))
    b = [a[x:x+3] for x in xrange(0, len(a), 3)]
    return render_template('3colportfolio.html', prods = b, count=0)

@app.route("/add")
def addToCart():
    cart_id =  request.args.get('cart-id')
    item_id = request.args.get('item-id')

    print cart_id, item_id

    c = session.get( 'count',0)
    p = session.get( 'items-' + cart_id ,[])
    p.append(item_id)

    session[ 'count'] = c +1
    session[ 'items-' + cart_id ] = p

    print session

    a = json.load( open( './json/toymatic_products.json'))
    b = [a[x:x+3] for x in xrange(0, len(a), 3)]

    return render_template('3colportfolio.html', prods = b, count = c )

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)
    app.debug = True
    app.run()

