
from flask import render_template, Blueprint,request, redirect, url_for, session


inventory_blueprint = Blueprint( 'inventory', __name__,url_prefix='/inventory')

@inventory_blueprint.route("/upload", methods=['GET','POST'])
def stores():
    if request.method == 'POST':
        data = request.form['data']
        from app import r
        r.set( 'toys', data)
    #json = open('./json/toymatic_products.json').read()
    return '200'

@inventory_blueprint.route("/get")
def get():
    import json
    from app import r
    return  json.dumps(json.loads(r.get('toys')),indent=4)

def parse_csv( a, b):
    with open( a, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            yield b(row)


def pp(x):
    if len(x) > 11:
        return (x[1],x[11])
    return (x[1],x[1])



template = """
{
    "id":"1",
    "title":"LEGO : Fire Ladder Set",
    "desc":"Hop in the fire ladder truck and race to the scene. Extend the ladder and put out the fire. Use the special stud shooting hose to battle the blaze and fight the flames on the ground with the fire extinguisher. Keep the oil barrel from exploding. It is up to you to protect the city.<br> Includes 2 mini figures a female fire fighter and a male fire fighter. <br>Features a fire ladder truck with extending ladder and hose, plus an oil barrel.<br>Move the fire ladder truck into position, extend the ladder and get above the fire.<br> Pull out the fire hose and shoot the water elements with the stud shooting function to put out the fire. Accessory elements include a fire extinguisher, shovel, circular saw, water studs and an axe.",
    "url":"",
    "price":"0.00",
    "image":"/static/images/1.jpg",
    "image_large":"/static/images/medium/1.jpg",
    "category":"",
    "ages":"1 -10",
    "develops":" motor skills",
    "amazon_link":"",
    "condition":"",
    "status":""
  },

"""