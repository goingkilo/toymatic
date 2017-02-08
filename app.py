import os
import redis
from flask import Flask, redirect, url_for
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
app.config['MAIL_USERNAME'] = 'goingkilo@gmail.com'
app.config['MAIL_PASSWORD'] = 'Erumai1!'
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

from module.dbish import  dbish_blueprint
app.register_blueprint( dbish_blueprint)

@app.route('/')
def index():
    return redirect( url_for( 'storefront.home'))



if __name__ == "__main__":
    app.run()

