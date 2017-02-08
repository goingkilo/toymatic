
from flask import render_template, Blueprint,request, redirect, url_for, session


inventory_blueprint = Blueprint( 'inventory', __name__,url_prefix='/store')

@inventory_blueprint.route("/", methods=['GET','POST'])
def stores():
    if request.method == 'POST':
        data = request.form['data']
        from store import r
        r.set( 'toys', data)
    #json = open('./json/toymatic_products.json').read()

    return '200'

