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
import json

import pandas as pd
from py2neo import Graph
from neo4j import GraphDatabase
import pdb

# TODO: move this to different file


def get_csv_dict(path='data/ingredient_autocomplete.csv'):
    ingredients = pd.read_csv(path, header=0).to_dict()
    return ingredients


def get_users(path='data/user_list.csv'):
    users = pd.read_csv(path, header=0).to_dict()
    return users


def get_recipes(path_1='data/test_query_output/q1_match_recipes.json',
                path_2='data/test_query_output/q2_content_based_filter.json',
                path_3='data/test_query_output/q3_collab_filter.json'):
    q1_match_recipes = open(path_1, encoding='utf-8-sig')
    q2_content_based = open(path_2, encoding='utf-8-sig')
    q3_match_recipes = open(path_3, encoding='utf-8-sig')

    results_array_1 = json.load(q1_match_recipes)
    results_array_2 = json.load(q2_content_based)
    results_array_3 = json.load(q3_match_recipes)

    matching_recipes = []

    for items in results_array_1:
        for item in items:
            for i in items[item]:
                matching_recipes.append(i)

    content_based = results_array_2

    collab_filter = results_array_3

    return matching_recipes, content_based, collab_filter


class PyNeoGraph:

    def __init__(self, uri='bolt://localhost:7687'):
        """
        """

        self.driver = Graph(bolt=True, host='localhost')

    def test_conn(self):
        query = """
                MATCH (n) 
                RETURN n LIMIT 5
                """
        results = self.driver.run(query).to_data_frame()

        if results.size == 5:
            return True
        else:
            return False

    def close(self):
        self.driver.close()

    def get_neo4j_id(self, node="(i:INGREDIENT)", in_list=[7213, 3184]):
        """
            Args:
                node(str): string in Cypher node format
                    (i:INGREDIENT) etc
                in_list(list): list of raw ids to match nodes

            Returns:
                ids(list): list of neo4j id fields for nodes

        """

        node_var, label = f"{node}".split(':')

        query = f"""
            MATCH {node}
            WHERE {node_var}.{label.lower()} IN {in_list}
            RETURN id({node_var})
        """

        return self.driver.run(query).to_series().to_list()

    def get_matching_recipes(self, main_ingredients = [7213, 3184], side_ingredients = [1170, 382, 5006]):
        """
            Args:
                main_ingredints(list[int]): list of main_ingredient raw_ids
                side_ingredient(list[int]): list of side_ingredient raw_ids

            Returns:
                results(list[dict]): list of matching recipes that contain main and side
                    ingredients
        """

        main_ingredients = self.get_neo4j_id(in_list=main_ingredients)
        side_ingredients = self.get_neo4j_id(in_list=side_ingredients)

        query = """
        MATCH path=(i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE)
        WITH r,
            collect(id(i)) AS ingredients,
            $main_ingredients AS main, // user input
            $side_ingredients AS side // user input
        WHERE all(x IN main
            WHERE (x IN ingredients))
            AND any(x IN side
            WHERE (x IN ingredients))
        WITH r.name as RecipeName, id(r) as ID
        ORDER BY size([x IN side WHERE (x) IN ingredients]) DESC, r.n_ingredients
        WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
        RETURN result[0..9]
        """

        results = self.driver.run(query, {"main_ingredients": main_ingredients,
                                    "side_ingredients": side_ingredients})
        return results.data()




def init_neo4j():
    driver = Graph(bolt=True, host='localhost')
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


def get_matching_recipes(driver, main_ingredients, side_ingredients):
    # TODO: implement the query
    # query = """
    #         """
    # results = driver.run(query).to_data_frame()
    # results = json.dumps(driver.run(query).data())

    results = [
        {
            "recipeName": "stuffed peppers with sausage",
            "recipeID": 434234
        },
        {
            "recipeName": "fresh tomato and roasted garlic salad dressing",
            "recipeID": 108091
        },
        {
            "recipeName": "strip salad",
            "recipeID": 41284
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

    results = json.dumps(results)
    results = {'data': results}

    return results


def get_additional_ingredients(driver, user_id, main_ingredients, side_ingredients):
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
