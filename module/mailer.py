

from flask import Blueprint,request, redirect, url_for, session
from flask_mail import Message
from module.store import  Cart
from sparkpost import SparkPost
import os



mailer_blueprint = Blueprint( 'mailer', __name__,url_prefix='/mailer')

def send():
    sparky = SparkPost() # uses environment variable
    from_email = 'admin@' + os.environ.get('SPARKPOST_SANDBOX_DOMAIN') # 'test@sparkpostbox.com'

    if request.method == 'POST':
        email = request.form['email'] or 'none-provided'
        phone = request.form['phone'] or 'none-provided'
        choice = request.form['optradio'] or 'none-provided'

        message = " requestor : email :" + email + "  phone number :" + phone  + " : toy choice :" + choice
        response = sparky.transmission.send(
            use_sandbox=True,

            recipients=['pavithra.ramesh@gmail.com'],
            html='<html><body><p>'+message+'</p></body></html>',
            from_email=from_email,
            subject='Customer wants'
        )

        cart = session.get('cart', Cart())
        cart.remove_item( choice)
        session['cart'] = cart

        print response
    return redirect(url_for('storefront.home'))

@mailer_blueprint.route("/mail", methods=['POST'])
def senad():
    print 'sending mail'
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        toys_in_basket =  [ x for x in request.form.keys() if x.startswith('toy')]
        print toys_in_basket
        choice = request.form['optradio']

        msg = Message( "Toymatic toy request ", sender=('Toymatic Corp',"toymatic.in@gmail.com"), recipients=['goingkilo@gmail.com','pavithra.ramesh@gmail.com'])
        msg.body = " requestor : email :" + email + "  phone number :" + phone  + " : toy choice :" + choice + '\n'
        msg.body += '\n'.join( toys_in_basket)

        print msg.body

        cart = session.get('cart', Cart())
        print 'removing from cart',cart
        cart.remove_item( choice)
        session['cart'] = cart
        print 'removinged from cart',cart, choice
        from app import mail
        mail.send(msg)
    return redirect(url_for('storefront.home'))

