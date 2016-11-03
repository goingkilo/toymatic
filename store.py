from flask import Flask,session, redirect, url_for, escape, request,Response,jsonify
from flask import render_template

from flask.ext.login import LoginManager
from flask.ext.login import login_required

import json


app = Flask(__name__)

# login_manager = LoginManager(app)
# login_manager.init_app(app)

#####################################################################
###################     THINK INSIDE THE BOX      ###################
#####################################################################
import pagehelper
pages = pagehelper.getpages()

@app.route("/rohn")
def rohn():
    page_num = request.args.get("page")
    print page_num
    page_num = int(page_num)
    page1 =  pages[ page_num % len(pages)]
    page1 = page1.split('\n')
    pagenums = len(pages)
    print len(page1)
    return render_template( 'srohn.html', page = page1, numpages=pagenums, selectedpage=page_num)


@app.route('/stocks')
def stocks():
    # from  yahoo_finance import Share
    # import datetime
    # from datetime import timedelta
    # today = str(datetime.date.today())
    # seven_days_ago = str( datetime.date.today() - timedelta( days=7))
    # boa = Share('BAC')
    # data = boa.get_historical( seven_days_ago, today)
    # print data
    # f = open('stocks.json','w')
    # json.dump( data, f)
    # f.close()
    data = json.load( open( 'stocks.json'))
    return render_template('stocks.html',data=data)

@app.route('/data')
def data():
    return open('static/d3.csv').read()

@app.route("/store")
def store():
    import fk
    prods = fk.load_products('home_improvement_tools_')
    c = fk.load_categories()
    return render_template('store.html',categories=c,products=prods )

@app.route("/map" ,methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        from geopy.geocoders import Nominatim
        geolocator = Nominatim()
        searchterm = request.form['searchterm']
        print searchterm
        location = geolocator.geocode( searchterm)
        lat1 = location.raw['lat']
        lon1 = location.raw['lon']
        return render_template('map.html', coords=json.dumps([lat1,0,lon1,0]) )
    lat1 = request.args.get('lat1');
    lon1 = request.args.get('lon1');
    lat2 = request.args.get('lat2');
    lon2 = request.args.get('lon2');
    print lat1,lat2,lon1,lon2
    return render_template('map.html', coords=json.dumps([lat1,lat2,lon1,lon2]) )

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()

