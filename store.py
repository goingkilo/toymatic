
from flask import Flask, session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template
#from flask_session import Session
from redis_session import RedisSessionInterface
import json,os,redis
from shopping_cart import Cart

from flask_login import LoginManager,login_required,login_user,UserMixin,logout_user

from flask import Flask,flash
from flask_bcrypt import Bcrypt

# --- --- --- --- --- --- APP STUFF  --- --- --- --- ---
app = Flask(__name__)

# --- --- --- --- --- --- REDIS STUFF  --- --- --- --- ---
connection_string  = os.environ.get('REDIS_URL','redis://localhost:6379')
r = redis.from_url(connection_string)

app.secret_key = os.urandom(24)

#redis sessions
app.session_interface = RedisSessionInterface(redis=r)
#app.config['SESSION_TYPE'] = 'filesystem'
#sess = Session()
#sess.init_app(app)

app.debug = True
# --- --- --- --- --- --- AUTH STUFF  --- --- --- --- ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)

r.set('user_a@b.c', bcrypt.generate_password_hash('hunter2'))
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

        return str(cart.get_item_count())
    else:
        p = products(3);
        cart = session.get( 'cart', Cart() )
        print cart.items
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

## -------------- auth stuff ---------

class User( UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    a = r.get('user_'+user_id)

    if a:
        return User(user_id)

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        userid = request.form['username']
        password = request.form['password']

        user = User(userid)
        stored_hash = r.get('user_'+userid)
        if not stored_hash:
            return abort(401)

        if not bcrypt.check_password_hash( stored_hash, password):
            return abort(402)

        login_user(user)

        session.pop('_flashes', None)
        flash('Logged in successfully.')

        next = request.args.get('next') or '/'
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('home'))

@app.route("/user/home")
@login_required
def user_home():
    user_id = request.args.get('user_id')
    cart = session.get('cart')

    return render_template('account.html', user='user user user', count=cart.get_item_count() or 0)

@app.route('/auth/register', methods=[ 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email    = request.form['email']
        password = request.form['password']
        confirm  = request.form['confirm-password']

        if password != confirm :
            session.pop('_flashes', None)
            session.pop('_flashes', None)
            flash(' passwords do not match ','error' )
            return render_template('login.html')

        r.set( 'user_' + email,  bcrypt.generate_password_hash(password))

        return redirect(url_for('login'))

# https://github.com/maxcountryman/flask-login

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def is_safe_url(x):
    return True

if __name__ == "__main__":
    app.run()

