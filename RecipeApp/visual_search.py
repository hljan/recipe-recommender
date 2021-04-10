from flask import Blueprint, render_template
from flask_login import login_required

visualSearch = Blueprint('visualSearch', __name__)


@visualSearch.route('/visualSearch/<user_id>/matching_recipes')
# @login_required
def matching_recipes(user_id):

    return render_template('visual_search.html', user_id=user_id)
