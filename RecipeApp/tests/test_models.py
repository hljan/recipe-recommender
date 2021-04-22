import pytest

from pathlib import Path
import time
from glob import glob
import pdb
import json

# TODO: track Query performance
# start = time.time()
# print("hello")
# end = time.time()
# print(end - start)


class RecipeQuery:
    def __init__(self, neo4j_driver):

        self.graph = neo4j_driver
        self.query_paths = self.get_query_paths(Path("data\\01_Queries"))
        self.query_results = self.get_query_results(Path("data\\01_Queries"))

    def get_query_paths(self, query_path):
        queries = (glob((query_path / '*/*.cypher').as_posix()))
        return queries

    def get_query_results(self, query_path):
        results = (glob((query_path / '*/*.json').as_posix()))
        return results

    def get_file(self, file_path):

        with open(file_path, mode='r', newline='\n') as f:
            out_file = f.read()

        return out_file


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
    query = recipe_q.get_query(recipe_q.query_paths[0])

    results = neo4j_driver.driver.run(query)
    assert len(results[0]['result[0..10]']) == 10


def test_get_matching_recipes(neo4j_driver):

    # recipe_q = RecipeQuery(neo4j_driver)
    # query_result = recipe_q.get_file(recipe_q.query_results[0])
    # query_result = json.loads(query_result)
    # issues reading json files?

    results = [
        {
            "result[0..9]": [
                {
                    "recipeName": "stuffed peppers with sausage",
                    "recipeID": 434234
                },
                {
                    "recipeName": "strip salad",
                    "recipeID": 41284
                },
                {
                    "recipeName": "fresh tomato and roasted garlic salad dressing",
                    "recipeID": 108091
                },
                {
                    "recipeName": "spinach and mushroom pizza",
                    "recipeID": 39912
                },
                {
                    "recipeName": "linguine with tomatoes and basil",
                    "recipeID": 110808
                },
                {
                    "recipeName": "zucchini packets for the grill",
                    "recipeID": 41087
                },
                {
                    "recipeName": "roasted tomato salad",
                    "recipeID": 63172
                },
                {
                    "recipeName": "linguini alla cecca",
                    "recipeID": 27118
                },
                {
                    "recipeName": "pasta w  garlic and veggies",
                    "recipeID": 46991
                }
            ]
        }
    ]

    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil',
                        '382&cheese', '5006&basil']  # raw_ids

    query_result = neo4j_driver.test_get_matching_recipes(
        main_ingredients, side_ingredients)

    result = neo4j_driver.get_matching_recipes(
        main_ingredients, side_ingredients)
    assert query_result == result


def test_q2(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[1])
    res = neo4j_driver.driver.run(query)
    data = res.data()
    result = data[0]['result[0..10]']
    # assert len(result) == 10
    assert len(result) == 2


def test_get_content_based_recipes(neo4j_driver):

    results = [
        {
            "result[0..9]": [  # TODO: change to 0..10 in UI
                {
                    "recipeName": "zucchini packets for the grill",
                    "recipeID": 41087
                },
                {
                    "recipeName": "nancy duke s ratatouille",
                    "recipeID": 93260
                }
            ]
        }
    ]
    user = 2203
    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil', '382&cheese', '5006&basil']

    query_result = neo4j_driver.get_content_based_recipes(
        user, main_ingredients, side_ingredients)

    result = neo4j_driver.get_content_based_recipes(
        user, main_ingredients, side_ingredients)

    assert len(result['data']) > 0
    # assert result == query_result


def test_q3(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[2])
    res = neo4j_driver.driver.run(query)
    data = res.data()

    result = data[0]['result[0..10]']
    # assert len(result) == 10
    assert len(result) == 2


def test_get_collaborative_recipes(neo4j_driver):
    results = [
            {
                "result[0..9]": [
                    {
                        "recipeName": "fresh tomato and roasted garlic salad dressing",
                        "recipeID": 108091
                    },
                    {
                        "recipeName": "zucchini marinara   diabetic",
                        "recipeID": 86077
                    },
                    {
                        "recipeName": "so easy pasta with fresh herbs and cold tomato",
                        "recipeID": 139450
                    },
                    {
                        "recipeName": "savory garbanzo beans over couscous",
                        "recipeID": 50730
                    },
                    {
                        "recipeName": "roasted tomato salad",
                        "recipeID": 63172
                    },
                    {
                        "recipeName": "azteca soup adopted",
                        "recipeID": 3614
                    },
                    {
                        "recipeName": "tofu parmesan",
                        "recipeID": 23997
                    },
                    {
                        "recipeName": "quick   easy chicken in wine sauce",
                        "recipeID": 89598
                    },
                    {
                        "recipeName": "grecian lamb with vegetables",
                        "recipeID": 89997
                    }
                ]
            }
        ]


    user = 2203
    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil', '382&cheese', '5006&basil']

    result = neo4j_driver.get_collaborative_recipes(
        user, main_ingredients, side_ingredients)

    assert len(result['data']) > 0


def test_q4(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[3])
    res = neo4j_driver.driver.run(query)
    data = res.data()

    result = data[0]['result[0..10]']
    # assert len(result) == 10
    # assert len(result) == 2


def test_get_additional_ingredients(neo4j_driver):
    results = [
            {
                "res[0..9]": [
                    {
                        "ingredientID": 5010,
                        "ingredientName": "onion"
                    },
                    {
                        "ingredientID": 5006,
                        "ingredientName": "olive oil"
                    },
                    {
                        "ingredientID": 6270,
                        "ingredientName": "salt"
                    },
                    {
                        "ingredientID": 5319,
                        "ingredientName": "pepper"
                    },
                    {
                        "ingredientID": 7655,
                        "ingredientName": "water"
                    },
                    {
                        "ingredientID": 6276,
                        "ingredientName": "salt and pepper"
                    },
                    {
                        "ingredientID": 5180,
                        "ingredientName": "parmesan cheese"
                    },
                    {
                        "ingredientID": 6335,
                        "ingredientName": "scallion"
                    },
                    {
                        "ingredientID": 840,
                        "ingredientName": "butter"
                    }
                ]
            }
        ]



def test_q5(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[4])
    res = neo4j_driver.driver.run(query)
    data = res.data()

    result = data[0]['result[0..10]']
    # assert len(result) == 10
    # assert len(result) == 2


def test_q6(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[5])
    res = neo4j_driver.driver.run(query)
    data = res.data()

    result = data[0]['result[0..10]']
    # assert len(result) == 10
    # assert len(result) == 2


def test_q7(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[6])
    res = neo4j_driver.driver.run(query)
    data = res.data()

    result = data[0]['result[0..10]']
    # assert len(result) == 10
    # assert len(result) == 2
