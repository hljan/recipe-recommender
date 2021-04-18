from flask import Blueprint, render_template, request
from models import PyNeoGraph, get_csv_dict
from flask_login import login_required

visualSearch = Blueprint('visualSearch', __name__)
main_ingredients = list()
side_ingredients = list()
selected_recipe = list()
driver_neo4j = list()


@visualSearch.route('/visualSearch/<user_id>/matching_recipes', methods=['GET', 'POST'])
# @login_required
def matching_recipes(user_id):
    global main_ingredients, side_ingredients, driver_neo4j

    if not main_ingredients or not side_ingredients:
        main_ingredients = request.args.get('main_ingredients')
        side_ingredients = request.args.get('side_ingredients')

        main_ingredients = list(main_ingredients.split(","))
        side_ingredients = list(side_ingredients.split(","))

    if not driver_neo4j:
        driver_neo4j = PyNeoGraph(debug=True)

    try:
        tab_type = request.form['tab_type']
    except:
        tab_type = 'recipe'

    if tab_type == 'recipe':
        result = driver_neo4j.get_matching_recipes(main_ingredients, side_ingredients)
    elif tab_type == 'ingredient':
        result = driver_neo4j.get_additional_ingredients(main_ingredients, side_ingredients)
    elif tab_type == 'contentBased':
        result = driver_neo4j.get_content_based_recipes(user_id, main_ingredients, side_ingredients)
    elif tab_type == 'collaborative':
        result = driver_neo4j.get_collaborative_recipes(user_id, main_ingredients, side_ingredients)

    return render_template('visual_search.html', user_id=user_id, tab_type=tab_type, result=result,
                           main_ingredients=main_ingredients, side_ingredients=side_ingredients)


@visualSearch.route('/visualSearch/<user_id>/recipe_info/<recipe>', methods=['GET', 'POST'])
# @login_required
def recipe_info(user_id, recipe):
    global main_ingredients, side_ingredients, driver_neo4j

    recipe_id, recipe_name = recipe.split("&")

    if not main_ingredients or not side_ingredients:
        main_ingredients = request.args.get('main_ingredients')
        side_ingredients = request.args.get('side_ingredients')

        main_ingredients = list(main_ingredients.split(","))
        side_ingredients = list(side_ingredients.split(","))

    if not driver_neo4j:
        driver_neo4j = PyNeoGraph(debug=True)

    try:
        tab_type = request.form['tab_type']
    except:
        tab_type = 'usedIngredients'

    if tab_type == 'usedIngredients':
        result = driver_neo4j.get_relevant_ingredients(recipe_id)
    elif tab_type == 'userRatings':
        result = driver_neo4j.get_relevant_ratings(user_id, recipe_id)

    return render_template('visual_search_recipe.html', user_id=user_id, recipe=recipe, tab_type=tab_type,
                           result=result, main_ingredients=main_ingredients, side_ingredients=side_ingredients)
