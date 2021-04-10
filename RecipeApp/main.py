from flask import Blueprint, render_template, request, redirect, url_for
from models import get_csv_dict

# from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/main/<user_id>', methods=['GET', 'POST'])
# @login_required
def initial_search(user_id):
    if request.method == 'GET':
        ingredient_dict = get_csv_dict('data/ingredient_list.csv')
        return render_template('main.html', user_id=user_id, ingredients=ingredient_dict)
    elif request.method == 'POST':
        main_ingredients = request.form['main_ingredients']
        side_ingredients = request.form['side_ingredients']
        print(main_ingredients)
        print(side_ingredients)

        if request.form['search_type'] == 'visual_search':
            return redirect(url_for('visualSearch.matching_recipes', user_id=user_id))
        elif request.form['search_type'] == 'text_search':
            return redirect(url_for('textSearch.text_search'))
