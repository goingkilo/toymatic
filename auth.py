

from store import app, r
from flask import request, abort, render_template, session, url_for, flash, redirect

from flask_login import LoginManager,login_required,login_user,UserMixin,logout_user
from flask_bcrypt import Bcrypt


# --- --- --- --- --- --- AUTH STUFF  --- --- --- --- ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


bcrypt = Bcrypt(app)

r.set('user_a@b.c', bcrypt.generate_password_hash('hunter2'))

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

