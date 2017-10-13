
from flask import render_template, Blueprint, request

gallery_blueprint = Blueprint( 'gallery', __name__, url_prefix='/gallery')

@gallery_blueprint.route("/home")
def home():
    return render_template( 'gallery/gallery.html')
    #return render_template('paper/paper.html')


@gallery_blueprint.route("/all")
def all():
    images = [x for x in open('images.txt').read().split('\n') if x]
    return render_template( 'gallery/all.html', imugs = images)

