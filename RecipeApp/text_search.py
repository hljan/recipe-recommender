import json

from flask import Blueprint, render_template, request
from flask_login import login_required

from models import PyNeoGraph

textSearch = Blueprint('textSearch', __name__)
main_ingredients = list()
side_ingredients = list()
selected_recipe = list()
driver_neo4j = list()

@textSearch.route('/text_search/<user_id>', methods=['GET', 'POST'])
# @login_required
def text_search(user_id):
    global main_ingredients, side_ingredients, driver_neo4j
    main_ingredients = list()
    side_ingredients = list()

    if not main_ingredients or not side_ingredients:
        main_ingredients = request.args.get('main_ingredients')
        side_ingredients = request.args.get('side_ingredients')

        main_ingredients = list(set((main_ingredients.split(","))))
        side_ingredients = list(set(side_ingredients.split(",")))

    if not driver_neo4j:
        driver_neo4j = PyNeoGraph(debug=True)

    result_1 = driver_neo4j.get_matching_recipes(main_ingredients, side_ingredients)
    matching_recipes = []
    for data in result_1:
        matching_recipes = json.loads(result_1[data])

    result_2 = driver_neo4j.get_content_based_recipes(user_id, main_ingredients, side_ingredients)
    content_based = []
    for data in result_2:
        content_based = json.loads(result_2[data])

    result_3 = driver_neo4j.get_collaborative_recipes(user_id, main_ingredients, side_ingredients)
    collab_filter = []
    for data in result_3:
        collab_filter = json.loads(result_3[data])

    return render_template('text_search.html',user_id=user_id, matching_recipes=matching_recipes,
                           main_ingredients=main_ingredients, side_ingredients=side_ingredients,
                           collab_filter=collab_filter, content_based=content_based)
