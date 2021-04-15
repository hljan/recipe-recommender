from flask import Blueprint, render_template
from flask_login import login_required
from models import get_recipes

textSearch = Blueprint('textSearch', __name__)


@textSearch.route('/text-search/<user_id>')
# @login_required
def text_search(user_id):
    matching_recipes, content_based, collab_filter = get_recipes()
    return render_template('text_search.html',user_id=user_id, matching_recipes=matching_recipes,
                           content_based=content_based, collab_filter=collab_filter)
