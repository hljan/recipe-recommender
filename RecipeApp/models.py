import pandas as pd
from py2neo import Graph
from neo4j import GraphDatabase


def get_csv_dict(path='data/ingredient_list.csv'):
    ingredients = pd.read_csv(path, header=0).to_dict()
    return ingredients


def init_neo4j(uri='bolt://localhost:7687', auth=('neo4j', 'recipe')):
    driver = Graph(bolt=True, host='localhost', user=auth[0], password=auth[-1])
    # driver = GraphDatabase.driver(uri=uri, auth=auth)
    return driver


def test_conn(driver):
    query = """
            MATCH (n) 
            RETURN n LIMIT 5
            """
    results = driver.run(query).to_data_frame()

    if results.size == 5:
        return True
    else:
        return False


def get_matching_recipes(driver, user_id, main_ingredients, side_ingredients):
    # TODO: implement the query
    results = main_ingredients
    # query = """
    #         """
    # results = driver.run(query).to_data_frame()

    return results


def get_alternative_ingredients(driver, user_id, main_ingredients, side_ingredients):
    # TODO: implement the query
    results = side_ingredients
    # query = """
    #         """
    # results = driver.run(query).to_data_frame()

    return results


def get_relevant_recipes(driver, user_id, recipe_id):
    # TODO: implement the query
    results = recipe_id
    # query = """
    #         """
    # results = driver.run(query).to_data_frame()

    return results


def get_relevant_ingredients(driver, user_id, recipe_id):
    # TODO: implement the query
    results = recipe_id
    # query = """
    #         """
    # results = driver.run(query).to_data_frame()

    return results


def get_relevant_ratings(driver, user_id, recipe_id):
    # TODO: implement the query
    results = recipe_id
    # query = """
    #         """
    # results = driver.run(query).to_data_frame()

    return results


def get_recipe_details(driver, recipe_id):
    # TODO: implement the query
    results = recipe_id
    # query = """
    #         """
    # results = driver.run(query).to_data_frame()

    return results
