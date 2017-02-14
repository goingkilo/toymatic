
import json,os,redis
from flask import Flask, Blueprint,session, redirect, url_for, escape, request,Response,jsonify,flash,render_template


store_blueprint = Blueprint( 'storefront', __name__,url_prefix='/store')


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self , item_id):
        if not item_id in self.items:
            self.items.append(item_id)

    def get_items(self):
        return self.items

    def get_item_count(self):
        return len(self.items)

    def remove_item(self, item_id):
        if self.items:
            if item_id in self.items:
                self.items.remove(item_id)
            return item_id

    def __repr__(self):
        s = ''
        for i in self.items:
            s += i +','
        return s

@store_blueprint.route( "/home", methods=['GET', 'POST'])
def home():
    p = products(4);
    cart = session.get( 'cart', Cart() )
    #print 'cart items', cart.items
    return render_template('store/home.html', prods = p, count=cart.get_item_count(), user='a@b.c')

@store_blueprint.route("/item")
def item():
    all_products = products(0)

    item_id = request.args.get('id')
    prduct = filter( lambda x : x['id'] == str(item_id) , all_products)
    cart = session.get( 'cart',Cart())
    other_images = prduct[0]['secondary_images'].split(',')
    return  render_template('store/item.html', p=prduct[0], others=other_images, count=cart.get_item_count())

@store_blueprint.route("/cart/delete")
def rem_item():
    item_id = request.args.get('item_id')
    cart = session.get('cart', None)
    if cart:
        cart.remove_item(item_id)
    return checkout()

@store_blueprint.route( '/cart/add', methods = ["POST"])
def add_item():
    cart = session.get( 'cart', Cart() )
    item_id = request.form['item-id']
    if item_id:
        cart.add_item(item_id)
    session[ 'cart'] = cart
    return str(cart.get_item_count())

@store_blueprint.route( '/cart/show')
def show_cart():
    cart = session.get( 'cart', Cart() )
    from flask import jsonify
    return jsonify(str(cart))

@store_blueprint.route("/checkout", methods = ["GET","POST"])
def checkout():
    if request.method == "GET":
        cart = session.get('cart', None)
        ret = []
        if not cart:
            return  render_template('store/checkout.html', products=ret, count=0)
        else:
            items = cart.get_items()
            p = products(0)

            for i in items:
                p1 = filter( lambda x : x['id'] == str(i) , p)
                ret.append(p1[0])

            return  render_template('store/checkout.html', products=ret, count=cart.get_item_count())
    else :
        return redirect( url_for('home'))

def products(batch_size=1):
    from app import r
    a = json.load( open( './json/a.json'))
    if batch_size == 0:
        return a
    b = [a[x:x+batch_size] for x in xrange(0, len(a), batch_size)]
    return b



