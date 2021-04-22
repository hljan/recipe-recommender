from flask import Blueprint, render_template, request, redirect, url_for
from models import get_csv_dict, PyNeoGraph

# import pdb

main = Blueprint('main', __name__)
ingredients_dict = dict()
driver_neo4j = list()
main_ingredients = list()
side_ingredients = list()


@main.route('/main/<user_id>', methods=['GET', 'POST'])
def initial_search(user_id):
    if request.method == 'GET':
        global ingredients_dict, driver_neo4j, main_ingredients, side_ingredients

        if not ingredients_dict:
            ingredients_dict = get_csv_dict()

        if not driver_neo4j:
            is_db_up = False
            try:
                driver_neo4j = PyNeoGraph()
                is_db_up = driver_neo4j.test_conn()

                # pdb.set_trace()
            except:
                pass
            return render_template('main.html', user_id=user_id, ingredients=ingredients_dict, db_connected=is_db_up)
        else:
            return render_template('main.html', user_id=user_id, ingredients=ingredients_dict, db_connected=True)

    elif request.method == 'POST':
        main_ingredients = request.form['main_ingredients'][:-1]
        side_ingredients = request.form['side_ingredients'][:-1]

        if request.form['search_type'] == 'visual_search':
            return redirect(url_for('visualSearch.matching_recipes', user_id=user_id,
                                    main_ingredients=main_ingredients, side_ingredients=side_ingredients))
        elif request.form['search_type'] == 'text_search':
            return redirect(url_for('textSearch.text_search', user_id=user_id,
                                    main_ingredients=main_ingredients, side_ingredients=side_ingredients))


@main.route('/main/<user_id>/recipe_details/<recipe>', methods=['GET', 'POST'])
def recipe_details(user_id, recipe):
    global driver_neo4j, main_ingredients, side_ingredients

    recipe_id, recipe_name = recipe.split("&")
    recipe_decode = recipe.replace('%20', ' ')

    if not driver_neo4j:
        driver_neo4j = PyNeoGraph(debug=False)

    result_1 = driver_neo4j.get_recipe_details(int(recipe_id))
    result_2 = driver_neo4j.get_relevant_ingredients(int(recipe_id))
    result_3 = driver_neo4j.get_alternative_ingredients(int(recipe_id))
    result = {'data': result_1['data'] + ";" + result_2['data'] + ";" + result_3['data']}

    return render_template('recipe_details.html', user_id=user_id, recipe=recipe_decode, result=result,
                           main_ingredients=main_ingredients, side_ingredients=side_ingredients)
