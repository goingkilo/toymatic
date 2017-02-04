
from flask import render_template, Blueprint


paper_blueprint = Blueprint( 'paper', __name__,url_prefix='/paper')

@paper_blueprint.route("/")
def paper():
    return render_template('paper/paper.html')
