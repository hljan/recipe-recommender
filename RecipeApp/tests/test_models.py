import pytest
import ast

import time
from glob import glob
import pdb

import json
from functools import wraps


def clock_query(f):
    start = time.time()

    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    end = time.time()
    print(end - start)
    return wrapper


# @clock_query
def test_neo4j_conn(neo4j_driver):

    is_conn = neo4j_driver.test_conn()
    assert is_conn == True


@pytest.mark.skip()
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


def test_get_matching_recipes(neo4j_driver):

    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil',
                        '382&cheese', '5006&basil']  # raw_ids

    result = neo4j_driver.get_matching_recipes(
        main_ingredients, side_ingredients)
    # assert len(result[0]['result[0..10]']) == 10


def test_get_content_based_recipes(neo4j_driver):

    user = 2203
    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil', '382&cheese', '5006&basil']

    result = neo4j_driver.get_content_based_recipes(
        user, main_ingredients, side_ingredients)

    assert len(result['data']) > 0


def test_get_collaborative_recipes(neo4j_driver):

    user = 2203
    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil', '382&cheese', '5006&basil']

    result = neo4j_driver.get_collaborative_recipes(
        user, main_ingredients, side_ingredients)

    assert len(result['data']) > 0


def test_get_additional_ingredients(neo4j_driver):

    main_ingredients = ['7213&tomato', '3184&garlic']
    # side_ingredients = ['1170&olive oil', '382&cheese', '5006&basil']
    side_ingredients = []

    result = neo4j_driver.get_additional_ingredients(main_ingredients,
                                                     side_ingredients)
    assert len(result['data']) > 0
    # ['ingredientID', 'ingredientName']
    # pdb.set_trace()


def test_get_relevant_ingredients(neo4j_driver):

    recipe_id = 41284
    result = neo4j_driver.get_relevant_ingredients(recipe_id)
    assert len(result['data']) > 0


def test_get_recipe_details(neo4j_driver):
    recipe_id = 41284
    result = neo4j_driver.get_relevant_ingredients(recipe_id)
    assert len(result['data']) > 5


def test_get_relevant_ratings(neo4j_driver):

    user_id = 2203
    recipe_id = 41284
    result = neo4j_driver.get_relevant_ratings(user_id, recipe_id)

# def test_get_alternative_ingredients(neo4j_driver):
#     recipe_id = 41284
#     result = neo4j_driver.get_alternative_ingredients(recipe_id)
