# -*- coding: utf-8 -*-
"""
    Module Level Docstring


    TODO:
        Q1 - matching recipes (inputs are user-id and ingredients-id)
        Q2 - recipe-related recipes (input is recipe-id (and user-id?))
        Q3 - recipe-related user-rating ((input is recipe-id (and user-id?))
        Q4 - alternative/additional ingredients (inputs are user-id and ingredients-id)
        Q5 - recipe-related ingredients (input is recipe-id (and user-id?))
        
"""

import pandas as pd
from py2neo import Graph
from neo4j import GraphDatabase
import pdb

# TODO: move this to different file


def get_csv_dict(path='data/ingredient_list.csv'):
    ingredients = pd.read_csv(path, header=0).to_dict()
    return ingredients


def get_users(path='data/user_list.csv'):
    users = pd.read_csv(path, header=0).to_dict()
    return users


def init_neo4j(uri='bolt://localhost:7687', auth=('neo4j', 'recipe')):
    driver = Graph(bolt=True, host='localhost',
                   user=auth[0], password=auth[-1])
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

def match_recipes(driver, ingredients, user_id):
    """
        Using neo4j library

        Recipes which includes the input ingredients provided by the user

        Args:
            driver (neo4j.Neo4jDriver)

        Returns:
            results (list):

        Input:​ List of ingredients​
        Output:​ List of recipe ids​
    """
    
    # ingredients = ["tomato", "garlic", "cheese", "basil", "pasta", "olive oil"]
    query = """
        //Recipe Search

        MATCH (i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE)

        WHERE i.name IN $ingredients

        RETURN r.recipe, r.n_ingredients , count(*) as occ

        ORDER BY occ DESC, r.n_ingredients
        """
        
    df = driver.run(query, {"ingredients": ingredients}).to_data_frame()
    return df

