from flask import Blueprint, render_template
from flask_login import login_required

textSearch = Blueprint('textSearch', __name__)


@textSearch.route('/text-search')
# @login_required
def text_search():
    return render_template('text_search.html')
