import json

from flask import Blueprint, render_template, request
from flask_login import login_required

from models import PyNeoGraph, get_recipes

textSearch = Blueprint('textSearch', __name__)
main_ingredients = ''
side_ingredients = ''
selected_recipe = ''
driver_neo4j = ''

@textSearch.route('/text-search/<user_id>/text_search', methods=['GET', 'POST'])
# @login_required
def text_search(user_id):
    global main_ingredients, side_ingredients, driver_neo4j

    if not main_ingredients or not side_ingredients:
        main_ingredients = request.args.get('main_ingredients')
        side_ingredients = request.args.get('side_ingredients')

        main_ingredients = list(main_ingredients.split(","))
        side_ingredients = list(side_ingredients.split(","))

    if not driver_neo4j:
        driver_neo4j = PyNeoGraph(debug=True)

    content_based, collab_filter = get_recipes()
    results = driver_neo4j.get_matching_recipes(main_ingredients, side_ingredients)

    for data in results:
        matching_recipes = json.loads(results[data])
    return render_template('text_search.html',user_id=user_id, matching_recipes=matching_recipes, matching_recipes_1=matching_recipes,
                           content_based=content_based, collab_filter=collab_filter, main_ingredients=main_ingredients,
                           side_ingredients=side_ingredients)
