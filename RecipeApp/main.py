from flask import Blueprint, render_template, request, redirect, url_for
from models import get_csv_dict, PyNeoGraph
import pdb

main = Blueprint('main', __name__)
ingredients_dict = dict()


@main.route('/main/<user_id>', methods=['GET', 'POST'])
def initial_search(user_id):
    if request.method == 'GET':
        global ingredients_dict

        if not ingredients_dict:
            ingredients_dict = get_csv_dict()

        is_db_up = False
        try:
            driver_py2neo = PyNeoGraph()
            is_db_up = driver_py2neo.test_conn()

            # pdb.set_trace()
        except:
            pass
        return render_template('main.html', user_id=user_id, ingredients=ingredients_dict, db_connected=is_db_up)

    elif request.method == 'POST':
        main_ingredients = request.form['main_ingredients'][:-1]
        side_ingredients = request.form['side_ingredients'][:-1]

        if request.form['search_type'] == 'visual_search':
            return redirect(url_for('visualSearch.matching_recipes', user_id=user_id,
                                    main_ingredients=main_ingredients, side_ingredients=side_ingredients))
        elif request.form['search_type'] == 'text_search':
            return redirect(url_for('textSearch.text_search', user_id=user_id,
                                    main_ingredients=main_ingredients, side_ingredients=side_ingredients))
