from flask import Blueprint, render_template, request, redirect, url_for, session
from models import get_csv_dict, init_neo4j, test_conn

# from flask_login import login_required

main = Blueprint('main', __name__)
ingredients_dict = dict()


@main.route('/main/<user_id>', methods=['GET', 'POST'])
# @login_required
def initial_search(user_id):
    if request.method == 'GET':
        global ingredients_dict
        driver_neo4j = session.get('driver_neo4j', None)

        if not ingredients_dict:
            ingredients_dict = get_csv_dict('data/ingredient_list.csv')

        if not driver_neo4j:
            is_db_up = False
            try:
                driver_neo4j = init_neo4j()
                # only check for the first time
                is_db_up = test_conn(driver_neo4j)
                session['driver_neo4j'] = driver_neo4j
            except:
                pass
            return render_template('main.html', user_id=user_id, ingredients=ingredients_dict, db_connected=is_db_up)
        else:
            session['driver_neo4j'] = driver_neo4j

        return render_template('main.html', user_id=user_id, ingredients=ingredients_dict, db_connected=True)

    elif request.method == 'POST':
        main_ingredients = request.form['main_ingredients'][:-1]
        side_ingredients = request.form['side_ingredients'][:-1]

        if request.form['search_type'] == 'visual_search':
            return redirect(url_for('visualSearch.query_by_ingredients', user_id=user_id, tab_type='recipe',
                                    main_ingredients=main_ingredients, side_ingredients=side_ingredients))
        elif request.form['search_type'] == 'text_search':
            return redirect(url_for('textSearch.text_search'))
