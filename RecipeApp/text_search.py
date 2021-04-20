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

    result = driver_neo4j.get_matching_recipes(main_ingredients, side_ingredients)

    matching_recipes =[]

    for data in result:
        matching_recipes = json.loads(result[data])

    return render_template('text_search.html',user_id=user_id, matching_recipes=matching_recipes,
                           main_ingredients=main_ingredients,
                           side_ingredients=side_ingredients)
