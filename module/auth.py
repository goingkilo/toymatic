from flask import  Flask, Blueprint, request, abort, render_template, session, url_for, flash, redirect
from flask_login import LoginManager,login_required,login_user,UserMixin,logout_user
from flask_bcrypt import Bcrypt


auth_blueprint = Blueprint( 'auth', __name__,url_prefix='/auth')

# --- --- --- --- --- --- AUTH STUFF  --- --- --- --- ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    a = r.get( user_id)
    if a:
        from module.auth import User
        return User(user_id)

# --- --- --- --- --- --- AUTH STUFF  --- --- --- --- ---
from app import  app
from app import  r
from app import login_manager

bcrypt = Bcrypt(app)
r.set('doggo@b.c', bcrypt.generate_password_hash('hunter2'))

class User( UserMixin):
    def __init__(self, id):
        self.id = id




@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    if request.method == 'POST':
        userid = request.form['username']
        password = request.form['password']

        user = User(userid)
        stored_hash = r.get(userid)
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

# @auth_blueprint.route("/user/home")
# @login_required
# def user_home():
#     user_id = request.args.get('user_id')
#     cart = session.get('cart')
#
#     return render_template('account.html', user='user user user', count=cart.get_item_count() or 0)

@auth_blueprint.route('/register', methods=[ 'POST'])
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

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def is_safe_url(x):
    return True

