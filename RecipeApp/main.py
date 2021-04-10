from flask import Blueprint, render_template, request, redirect, url_for
from models import get_csv_dict, init_neo4j, test_conn

# from flask_login import login_required

main = Blueprint('main', __name__)

ingredients_dict = dict()
main_ingredients = list()
side_ingredients = list()

driver_neo4j = ''


@main.route('/main/<user_id>', methods=['GET', 'POST'])
# @login_required
def initial_search(user_id):
    if request.method == 'GET':
        global ingredients_dict, driver_neo4j, session_neo4j

        if not ingredients_dict:
            ingredients_dict = get_csv_dict('data/ingredient_list.csv')

        if not driver_neo4j:
            driver_neo4j = init_neo4j()
            # only check for the first time
            is_db_up = test_conn(driver_neo4j)
            return render_template('main.html', user_id=user_id, ingredients=ingredients_dict, db_connected=is_db_up)

        return render_template('main.html', user_id=user_id, ingredients=ingredients_dict, db_connected=True)

    elif request.method == 'POST':
        global main_ingredients, side_ingredients

        main_ingredients = request.form['main_ingredients']
        side_ingredients = request.form['side_ingredients']

        main_ingredients = list(main_ingredients[:-1].split(","))
        side_ingredients = list(side_ingredients[:-1].split(","))

        if request.form['search_type'] == 'visual_search':
            return redirect(url_for('visualSearch.matching_recipes', user_id=user_id))
        elif request.form['search_type'] == 'text_search':
            return redirect(url_for('textSearch.text_search'))
