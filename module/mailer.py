
from flask import Blueprint,request, redirect, url_for, session
from flask_mail import Message
from module.store import  Cart


mailer_blueprint = Blueprint( 'mailer', __name__,url_prefix='/mailer')

@mailer_blueprint.route("/mail", methods=['POST'])
def send():
    print 'sending mail'
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        choice = request.form['optradio']
        msg = Message( "Toymatic !!", sender=('Toymatic Corp',"site-admin@toymatic.in"), recipients=['yesbob@gmail.com','pavithra.ramesh@gmail.com'])
        msg.body = "" + email + " / " + phone + "/ toy:" + choice
        cart = session.get('cart', Cart())
        cart.remove_item( choice)
        session['cart'] = cart
        #mail.send(msg)
    print 5
    return redirect(url_for('storefront.home'))

