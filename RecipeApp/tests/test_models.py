import pytest

from pathlib import Path
import time
from glob import glob
import pdb

# TODO: track Query performance
# start = time.time()
# print("hello")
# end = time.time()
# print(end - start)

class RecipeQuery:
    def __init__(self, neo4j_driver):

        self.graph = neo4j_driver
        self.query_paths = self.get_query_paths(Path("data\\01_Queries"))
        

    def get_query_paths(self, query_path):
        queries = (glob((query_path / '*/*.cypher').as_posix()))
        return queries

    def run_query(self, query_path):

        with open(query_path, mode='r', newline='\n') as f:
            query = f.read()

        res = self.graph.driver.run(query)

        return res.data()

def test_neo4j_conn(neo4j_driver):

    is_conn = neo4j_driver.test_conn()
    assert is_conn == True

def test_get_neo4j_id(neo4j_driver):
    main_ingredients = [7213, 3184]

    results = neo4j_driver.get_neo4j_id(in_list=main_ingredients)
    assert results == [226, 4246]

    side_ingredients = [1170, 382, 5006]

    results = neo4j_driver.get_neo4j_id(in_list=side_ingredients)
    assert results == [28, 173, 4341]

def test_q1(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    results = recipe_q.run_query(recipe_q.query_paths[0])
    assert len(results[0]['result[0..10]']) == 10

def test_get_matching_recipes(neo4j_driver):
    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['28&olive oil', '173&cheese', '4341&basil']
    results = neo4j_driver.get_matching_recipes(main_ingredients, side_ingredients)
