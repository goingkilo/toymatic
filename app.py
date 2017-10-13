import os
import redis
from flask import Flask, redirect, url_for, request, session, abort,render_template
from flask_mail import Mail

from flask_login import LoginManager,login_required,login_user,UserMixin,logout_user
from flask_bcrypt import Bcrypt

# --- --- --- --- --- --- APP STUFF  --- --- --- --- ---
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# --- --- --- --- --- --- REDIS STUFF  --- --- --- --- ---
from module.redis_session import RedisSessionInterface

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
app.config['MAIL_USERNAME'] = 'toymatic.in@gmail.com'
app.config['MAIL_PASSWORD'] = 'bommai@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail.init_app(app)


# --- --- --- --- --- --- REGISTER BLUEPRINTS --- --- --- --- ---

from module.mailer import mailer_blueprint
app.register_blueprint( mailer_blueprint)

from module.inventory import inventory_blueprint
app.register_blueprint( inventory_blueprint)

from module.store import  store_blueprint
app.register_blueprint( store_blueprint)

from module.paper import  paper_blueprint
app.register_blueprint( paper_blueprint)

#from module.auth import auth_blueprint
#app.register_blueprint( auth_blueprint)

from module.gallery import gallery_blueprint
app.register_blueprint( gallery_blueprint)
from module.dbish import  dbish_blueprint
app.register_blueprint( dbish_blueprint)

"""
# UNCOMMENT FOR CSRF PROTECTION. WARNING - FORMS WON'T WORK NO MO
@app.before_request
def csrf_protect():
    if request.method == "POST" and request.path != '/inventory/upload':
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = "str(os.urandom(24))"
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token
"""

@app.route('/store')
def store():
    return redirect( url_for( 'storefront.home'))

@app.route('/')
def index():
    return redirect( url_for( 'gallery.home'))
    #return redirect( '/static/gallery.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()

