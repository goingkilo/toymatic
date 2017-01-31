
from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template
#from flask_session import Session
from redis_session import RedisSessionInterface
import json,os,redis

from shopping_cart import Cart


# --- --- --- --- --- --- --- --- --- --- ---
app = Flask(__name__)

connection_string  = os.environ.get('REDIS_URL','redis://localhost:6379')
r = redis.from_url(connection_string)
print 'connectint to redis', r

app.secret_key = os.urandom(24)

#redis sessions
app.session_interface = RedisSessionInterface(redis=r)
#app.config['SESSION_TYPE'] = 'filesystem'
#sess = Session()
#sess.init_app(app)

app.debug = True
# --- --- --- --- --- --- --- --- --- --- ---


@app.route("/paper")
def paper():
    return render_template('paper.html')

@app.route( "/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        cart = session.get( 'cart', Cart() )
        print 'x',cart
        item_id = request.form['item-id']

        if item_id:
            cart.add_item(item_id)

        session[ 'cart'] = cart

        return "OK"
    else:
        p = products(3);
        cart = session.get( 'cart', Cart() )
        print cart.items
        return render_template('home.html', prods = p, count=cart.get_item_count())

@app.route("/item")
def item():
    all_products = products(0)
    item_id = request.args.get('id')
    prduct = filter( lambda x : x['id'] == str(item_id) , all_products)
    cart = session.get( 'cart',Cart())
    return  render_template('item.html', p=prduct[0] , count=cart.get_item_count())

@app.route("/cart/delete")
def rem_item():
    item_id = request.args.get('item_id')
    cart = session.get('cart', None)
    if cart:
        cart.remove_item(item_id)
    return checkout()


@app.route("/checkout")
def checkout():
    cart = session.get('cart', None)
    ret = []
    if not cart:
        return  render_template('checkout.html', products=ret, count=0)
    else:
        items = cart.get_items()
        p = products(0)

        for i in items:
            p1 = filter( lambda x : x['id'] == str(i) , p)
            ret.append(p1[0])

        return  render_template('checkout.html', products=ret, count=cart.get_item_count() or 0)

def products(batch_size=1):
    a = json.load( open( './json/toymatic_products.json'))
    if batch_size == 0:
        return a
    b = [a[x:x+batch_size] for x in xrange(0, len(a), batch_size)]
    return b

if __name__ == "__main__":
    app.run()

