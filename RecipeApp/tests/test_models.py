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


@pytest.mark.skip()
def test_run_q1(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_query(recipe_q.query_paths[0])

    results = neo4j_driver.driver.run(query)
    assert len(results[0]['result[0..10]']) == 10

def test_get_matching_recipes(neo4j_driver):

    # recipe_q = RecipeQuery(neo4j_driver)
    # query_result = recipe_q.get_file(recipe_q.query_results[0])
    # query_result = json.loads(query_result)
    main_ingredients = ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil', '382&cheese', '5006&basil'] #raw_ids

    query_result = neo4j_driver.test_get_matching_recipes(main_ingredients, side_ingredients)



    result = neo4j_driver.get_matching_recipes(
        main_ingredients, side_ingredients)
    pdb.set_trace()
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
    user = 2203
    main_ingredients =  ['7213&tomato', '3184&garlic']
    side_ingredients = ['1170&olive oil', '382&cheese', '5006&basil']

    result = neo4j_driver.get_content_based_recipes(user, main_ingredients, side_ingredients)

def test_q3(neo4j_driver):
    recipe_q = RecipeQuery(neo4j_driver)
    query = recipe_q.get_file(recipe_q.query_paths[2])
    res = neo4j_driver.driver.run(query)
    data = res.data()
  
    result = data[0]['result[0..10]']
    # assert len(result) == 10
    assert len(result) == 2

