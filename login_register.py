from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import Flask, Response
from flask.ext.login import LoginManager, UserMixin, login_required

from flask import render_template

app = Flask(__name__)

def is_logged_in(request):
    token = request.cookies.get('token')
    if not token:
        return False
    return True

def load_user(request):
    token = request.args.get('token')
    if token:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None


@app.route("/",methods=["GET"])
def index():
    if not is_logged_in(request):
        print '39'
        return render_template('login.html')
    return render_template('index.html')

@app.route("/logout")
def logout():
    redirect_to_index = redirect("/")
    response = app.make_response(redirect_to_index )
    response.set_cookie('token',value= '', expires=0)
    return response

def login_and_redirect_to( path, user):
    redirect_to_index = redirect(path)
    response = app.make_response(redirect_to_index )
    response.set_cookie('token',value='user:password')
    return render_template(path,email=user)

@app.route("/login",methods=['GET', 'POST'])
def do1():
    if request.method == 'POST':
        print 'log in request' ,request.form['email'] or 'None supplied' ,request.form['password'] or 'None supplied'
        user = load_user(request)
        return login_and_redirect_to('/index.html', "aha@oho.com")
    print '32'
    return render_template('login.html')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()
