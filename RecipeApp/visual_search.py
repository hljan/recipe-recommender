from flask import Blueprint, render_template, request, session
from models import get_matching_recipes, get_alternative_ingredients, \
    get_relevant_recipes, get_relevant_ingredients, get_relevant_ratings
from flask_login import login_required

visualSearch = Blueprint('visualSearch', __name__)
main_ingredients = ''
side_ingredients = ''
selected_recipe = ''
driver_neo4j = ''


@visualSearch.route('/visualSearch/<user_id>/given_ingredients/<tab_type>')
# @login_required
def query_by_ingredients(user_id, tab_type):
    global main_ingredients, side_ingredients, driver_neo4j

    if not main_ingredients or not side_ingredients:
        main_ingredients = request.args.get('main_ingredients')
        side_ingredients = request.args.get('side_ingredients')

        main_ingredients = list(main_ingredients.split(","))
        side_ingredients = list(side_ingredients.split(","))

    if not driver_neo4j:
        driver_neo4j = session.get('driver_neo4j', None)

    if tab_type == 'recipe':
        result = get_matching_recipes(driver_neo4j, user_id, main_ingredients, side_ingredients)
    elif tab_type == 'ingredient':
        result = get_alternative_ingredients(driver_neo4j, user_id, main_ingredients, side_ingredients)

    return render_template('visual_search_step1.html', user_id=user_id, tab_type=tab_type, result=result)


@visualSearch.route('/visualSearch/<user_id>/given_recipe/<tab_type>')
# @login_required
def query_by_recipe(user_id, tab_type):
    global selected_recipe, driver_neo4j

    if not selected_recipe:
        selected_recipe = request.args.get('selected_recipe')

    if not driver_neo4j:
        driver_neo4j = session.get('driver_neo4j', None)

    if tab_type == 'recipe':
        result = get_relevant_recipes(driver_neo4j, user_id, selected_recipe)
    elif tab_type == 'ingredient':
        result = get_relevant_ingredients(driver_neo4j, user_id, selected_recipe)
    elif tab_type == 'rating':
        result = get_relevant_ratings(driver_neo4j, user_id, selected_recipe)

    return render_template('visual_search_step2.html', user_id=user_id, tab_type=tab_type, result=result)
