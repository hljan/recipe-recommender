import pytest


import time
from glob import glob
import pdb
from .graph_fixture import PyNeoGraphUI, RecipeQuery
import json

# TODO: track Query performance
# start = time.time()
# print("hello")
# end = time.time()
# print(end - start)


def test_neo4j_conn(neo4j_driver):

    is_conn = neo4j_driver.test_conn()
    assert is_conn == True


def test_get_neo4j_id(neo4j_driver):
    main_ingredients = [7213, 3184]
    results = neo4j_driver.get_neo4j_id(in_list=main_ingredients)
    assert results == [226, 4246]

    # ['light maple syrup', 'apricot brandy', 'adobo sauce']
    side_ingredients = [28, 173, 4341]
    results = neo4j_driver.get_neo4j_id(in_list=side_ingredients)
    assert results == [1589, 2955, 6194]

    # ['olive oil', 'cheese', 'basil']
    side_ingredients = [1170, 382, 5006]
    results = neo4j_driver.get_neo4j_id(in_list=side_ingredients)
    assert results == [28, 173, 4341]


def test_run_q1(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[0])

    results = neo4j_driver.driver.run(query).data()
    assert len(results[0]['result[0..10]']) == 10


def test_get_matching_recipes(neo4j_driver):

    # recipe_q = RecipeQuery(neo4j_driver)
    # query_result = recipe_q.get_file(recipe_q.query_results[0])
    # query_result = json.loads(query_result)
    # issues reading json files?

    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil',
                        '382&cheese', '5006&basil']  # raw_ids

    result = neo4j_driver.get_matching_recipes(
        main_ingredients, side_ingredients)
    assert len(results[0]['result[0..10]']) == 10


def test_q2(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[1])
    res = neo4j_driver.driver.run(query)
    data = res.data()
    result = data[0]['result[0..10]']
    # assert len(result) == 10
    assert len(result) == 2


def test_get_content_based_recipes(neo4j_driver):

    user = 2203
    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil', '382&cheese', '5006&basil']

    result = neo4j_driver.get_content_based_recipes(
        user, main_ingredients, side_ingredients)

    assert len(result['data']) > 0
    # assert len(result['data']) > 0
    # assert result == query_result


def test_q3(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[2])
    res = neo4j_driver.driver.run(query)
    data = res.data()

    result = data[0]['result[0..10]']
    assert len(result) == 10


def test_get_collaborative_recipes(neo4j_driver):

    user = 2203
    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil', '382&cheese', '5006&basil']

    result = neo4j_driver.get_collaborative_recipes(
        user, main_ingredients, side_ingredients)

    assert len(result['data']) > 0


@pytest.mark.skip()
def test_q4(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[3])
    res = neo4j_driver.driver.run(query)
    data = res.data()

    result = data[0]['result[0..10]']
    assert len(result) == 10


def test_get_additional_ingredients(neo4j_driver):

    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil', '382&cheese', '5006&basil']

    result = neo4j_driver.get_additional_ingredients(main_ingredients,
                                                     side_ingredients)


def test_q5(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[4])
    res = neo4j_driver.driver.run(query)
    data = res.data()

    assert data[0].keys() is not None
    assert ['ingredientName', 'ingredientID'] == [i for i in data[0].keys()]

def test_get_relevant_ingredients(neo4j_driver):

    recipe_id = 41284
    results = neo4j_driver.get_relevant_ingredients(recipe_id)
    assert results['data'].keys() is not None
    assert ['ingredientName', 'ingredientID'] == [i for i in data['data'].keys()]


def test_q6(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[5])
    res = neo4j_driver.driver.run(query)
    data = res.data()
    result = data[0]

    assert ['steps', 'calorieLevel',
            'numberOfIngredients', 'nutritionDetials',
            'tags', 'avgRating', 'numberOfRatings'] == [i for i in result.keys()]


def test_q7(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[6])
    res = neo4j_driver.driver.run(query)
    data = res.data()

    result = data[0]['result[0..10]']
    assert len(result) == 10
