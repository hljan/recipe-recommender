from flask import Blueprint, render_template
from flask_login import login_required

visualSearch = Blueprint('visualSearch', __name__)


@visualSearch.route('/')
# @login_required
def visual_search():
    return render_template('visual_search.html')
