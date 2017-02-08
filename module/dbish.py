from flask import Flask,Blueprint, request
from flask_sqlalchemy import SQLAlchemy
import os, json


if os.environ.has_key('DATABASE_URL'):
    db_uri = os.environ['DATABASE_URL']
else :
    db_uri =  'postgresql://localhost:5432/monocle'

# register me yo !
dbish_blueprint = Blueprint( 'dbish', __name__,url_prefix='/db')

from app import app
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "lusers"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    role  = db.Column( db.String(10))
    address = db.Column(db.String(200))

    def __init__(self, username, email, role="user"):
        self.username = username
        self.email = email
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.username

"""
class UserCreds(db.Model):
    __tablename__ = "luser_creds"
    id = db.Column(db.Integer, primary_key=True)
    phash = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, username, email, role="user"):
        self.username = username
        self.email = email
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.username


class Toy(db.Model):
    __tablename__ = "my_toys"
    id = db.Column(db.Integer, primary_key = True)
    toy_desc = db.Column(db.String(120))
    toy_title = db.Column(db.String(120))
    toy_image = db.Column(db.String(120))
    toy_url = db.Column(db.String(120))
    toy_image = db.Column(db.String(120))
    toy_image_large = db.Column(db.String(120))
    toy_category = db.Column(db.String(120))
"""

@dbish_blueprint.route("/create")
def create():
    db.create_all()
    admin = User('admin', 'admin@toymatic.in',"admin")
    guest = User('guest', 'guest@toymatic.in')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    return "OK"


@dbish_blueprint.route("/get")
def get():
    users = User.query.all()
    ret = []
    for i in users:
        ret.append( "'" + str(i.id) + ","  + i.email + "'")
    return json.dumps(ret)


@dbish_blueprint.route("/update/", methods=["POST"])
def upd():
    if request.method == "POST":
        id = request.form['id']
        phash = request.form['pwd']
        users = User.query.filter_by( id=id)
        print users
        user = users.first()
        user.phash = phash
        db.session.add(user)
        db.session.commit()
    return "OK"


