
from flask import render_template, Blueprint,request, redirect, url_for, session
from flask_mail import Mail, Message
from shopping_cart import  Cart


mailer_blueprint = Blueprint( 'mailer', __name__,url_prefix='/mail')

#@app.route("/mail", methods=['POST'])
@mailer_blueprint.route("/", methods=['POST'])
def send():
    print 'sending mail'
    if request.method == 'POST':
        from store import mail
        print 2,request.form
        email = request.form['email']
        phone = request.form['phone']
        choice = request.form['optradio']
        print 3
        msg = Message( "Toymatic !!", sender=('Toymatic Corp',"site-admin@toymatic.in"), recipients=['yesbob@gmail.com','pavithra.ramesh@gmail.com'])
        msg.body = "" + email + " / " + phone + "/ toy:" + choice
        print 4
        cart = session.get('cart', Cart())
        cart.remove_item( choice)
        session['cart'] = cart
        #mail.send(msg)
    print 5
    return redirect(url_for('home'))

