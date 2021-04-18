import json

from flask import Blueprint, render_template, request
from models import PyNeoGraph

displayRecipe = Blueprint('displayRecipe', __name__)
driver_neo4j = ''

@displayRecipe.route('/recipe/<recipe_id>/<user_id>')

def display_recipe(user_id, recipe_id):
    global driver_neo4j

    if not driver_neo4j:
        driver_neo4j = PyNeoGraph(debug=True)

    results = driver_neo4j.get_recipe_details(recipe_id)

    recipe_details = []

    for data in results:
        recipe_details = json.loads(results[data])

    return render_template('display_recipe.html', user_id=user_id, recipe_id=recipe_id, recipe_details=recipe_details)