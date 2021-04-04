from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route('/')
# @login_required
def initial_search():
    return render_template('main.html')