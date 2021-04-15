from flask import Blueprint, render_template
from flask_login import login_required
from models import get_recipes_json

textSearch = Blueprint('textSearch', __name__)


@textSearch.route('/text-search/<user_id>')
# @login_required
def text_search(user_id):
    recipes = get_recipes_json()
    return render_template('text_search.html',user_id=user_id, recipes=recipes)
