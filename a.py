from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template

from flask.ext.login import LoginManager
from flask.ext.login import login_required

import json

app = Flask(__name__)
login_manager = LoginManager(app)

def laptops():
    a = json.load( open( 'womens_footwear.json'))
    b  = a['productInfoList']
    c = []
    e = []
    for i in b:
        d = {   }
        print json.dumps(i,indent=4)
        d['url'] = i['productBaseInfo']['productAttributes']['productUrl']
        d['brand'] = i['productBaseInfo']['productAttributes']['productBrand']
        d['color'] = i['productBaseInfo']['productAttributes']['color']
        d['title'] = i['productBaseInfo']['productAttributes']['title']
        d['image'] = i['productBaseInfo']['productAttributes']['imageUrls']['200x200']
        d['price'] = i['productBaseInfo']['productAttributes']['sellingPrice']
        d['id'] =  i['productBaseInfo']['productIdentifier']['productId']
        d['desc'] = i['productBaseInfo']['productAttributes']['productDescription']
        d['inStock'] =  i['productBaseInfo']['productAttributes']['inStock']
        d['available'] =   i['productBaseInfo']['productAttributes']['isAvailable']

        if len(e) == 3:
            c.append(e)
            e = []
        e.append(d) 
    print e
    return c

def parse_products():
    a = json.load( open( 'womens_footwear.json'))
    b  = a['productInfoList']
    c = []
    e = []
    for i in b:
        d = {   }
        print json.dumps(i,indent=4)
        d['url'] = i['productBaseInfoV1']['productUrl']
        d['brand'] = i['productBaseInfoV1']['productBrand']
        d['color'] = i['productBaseInfoV1']['attributes']['color']
        d['title'] = i['productBaseInfoV1']['title']
        d['image'] = i['productBaseInfoV1']['imageUrls']['200x200']
        d['price'] = i['productBaseInfoV1']['flipkartSpecialPrice']['amount']
        d['id'] =  i['productBaseInfoV1']['productId']
        d['desc'] = i['productBaseInfoV1']['productDescription']
        d['inStock'] =  i['productBaseInfoV1']['inStock']
        #d['available'] =   i['productBaseInfoV1']['productAttributes']['isAvailable']

        if len(e) == 3:
            c.append(e)
            e = []
        e.append(d)
    print e
    return c

def cats():
    a1 = json.load( open( 'categories.json'))
    b1 =  a1['apiGroups']['affiliate']['apiListings'].values()
    return b1

@app.route("/p/")
def prods():
    c = jsonify(b)
    """
    return Response(response=c,
    status=200, 
    mimetype="application/json")
    """
    return c

@app.route("/rohn")
def rohn():
    return render_template( 'srohn.html')

@app.route("/2")
def root():
    prods = parse_products()
    c = cats()
    return render_template('b.html',categories=c,products=prods )


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()

