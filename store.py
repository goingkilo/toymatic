
import json,os,redis
from flask import Flask, session, redirect, url_for, escape, request,Response,jsonify,flash,render_template

from shopping_cart import Cart
from flask_mail import Mail

# --- --- --- --- --- --- APP STUFF  --- --- --- --- ---
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# --- --- --- --- --- --- REDIS STUFF  --- --- --- --- ---
from redis_session import RedisSessionInterface

connection_string  = os.environ.get('REDIS_URL','redis://localhost:6379')
r = redis.from_url(connection_string)
app.session_interface = RedisSessionInterface(redis=r)
#app.config['SESSION_TYPE'] = 'filesystem'
#sess = Session()
#sess.init_app(app)

# --- --- --- --- --- --- MAIL STUFF  --- --- --- --- ---
mail = Mail()
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'goingkilo@gmail.com'
app.config['MAIL_PASSWORD'] = 'Erumai1!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail.init_app(app)

from mailer import mailer_blueprint
app.register_blueprint( mailer_blueprint)

from inventory import inventory_blueprint
app.register_blueprint( inventory_blueprint)

@app.route( "/", methods=['GET', 'POST'])
def home():
    p = products(4);
    cart = session.get( 'cart', Cart() )
    #print 'cart items', cart.items
    return render_template('home.html', prods = p, count=cart.get_item_count(), user='a@b.c')

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

@app.route( '/cart/add', methods = ["POST"])
def add_item():
    cart = session.get( 'cart', Cart() )
    item_id = request.form['item-id']
    if item_id:
        cart.add_item(item_id)
    session[ 'cart'] = cart
    return str(cart.get_item_count())


@app.route("/checkout", methods = ["GET","POST"])
def checkout():
    if request.method == "GET":
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

            return  render_template('checkout.html', products=ret, count=cart.get_item_count())
    else :
        return redirect( url_for('home'))

def products(batch_size=1):
    a = json.load( open( './json/toymatic_products.json'))
    if batch_size == 0:
        return a
    b = [a[x:x+batch_size] for x in xrange(0, len(a), batch_size)]
    return b




if __name__ == "__main__":
    app.run()

