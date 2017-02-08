
from flask import render_template, Blueprint
from flask_login import login_required

paper_blueprint = Blueprint( 'paper', __name__,url_prefix='/paper')

@paper_blueprint.route("/home")
# @login_required
def paper():
    return render_template('paper/paper.html')


@paper_blueprint.route('/map')
def maps():
    return render_template('paper/map.html')

@paper_blueprint.route('/stocks')
def stocks():
    return render_template('paper/stocks.html')


@paper_blueprint.route('/essays')
def essays():
    return render_template('paper/essays.html')