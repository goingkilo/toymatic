
from flask import render_template, Blueprint
from flask_login import login_required
import feedparser

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
    url = 'http://blog.fogus.me/feed/'
    d = feedparser.parse( url)
    d1 = [ { 'title':x['title'], 'author': x['author'], 'summary' : x['summary'], 'link': x['link']} for x in d.entries]
    return render_template('paper/essays.html', entries = d1)