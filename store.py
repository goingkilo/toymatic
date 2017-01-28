
from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template
from flask_session import Session

import json,os


app = Flask(__name__)

@app.route("/paper")
def paper():
    return render_template('paper.html')

@app.route( "/", methods=['GET', 'POST'])
def homeinve():

    p = products(3);


    if request.method == 'POST':
        item_id = request.form['item-id']

        items = session.get( 'items' ,[])
        items.append(item_id)

        item_count = session.get( 'item-count',0)
        item_count = item_count + 1
        print '--- -- -- item_count', item_count

        session[ 'item-count'] = item_count
        session[ 'items'] = items
        return "OK"
    item_count = session.get( 'item-count',0)
    return render_template('home.html', prods = p, count=item_count)

@app.route("/item")
def item():
    p = products(0)
    item_id = request.args.get('id')
    p1 = filter( lambda x : x['id'] == str(item_id) , p)
    return  render_template('item.html', p=p1[0])

@app.route("/checkout")
def checkout():
    items = session.get('items',[])
    p = products(0)
    ret = []
    for i in items:
        p1 = filter( lambda x : x['id'] == str(i) , p)
        ret.append(p1[0])
    print ret
    item_count = session.get( 'item-count',0)
    print item_count
    print items
    return  render_template('checkout.html', products=ret, count=item_count)



def products(batch_size=1):
    a = json.load( open( './json/toymatic_products.json'))
    if batch_size == 0:
        return a
    b = [a[x:x+batch_size] for x in xrange(0, len(a), batch_size)]
    return b

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)
    app.debug = True
    app.run()

