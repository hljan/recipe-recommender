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


def get_recipes(path_2='data/test_query_output/q2_content_based_filter.json',
                path_3='data/test_query_output/q3_collab_filter.json'):
    q2_content_based = open(path_2, encoding='utf-8-sig')
    q3_match_recipes = open(path_3, encoding='utf-8-sig')

    results_array_2 = json.load(q2_content_based)
    results_array_3 = json.load(q3_match_recipes)

    content_based = results_array_2

    collab_filter = results_array_3

    return content_based, collab_filter


class PyNeoGraph:

    def __init__(self, debug=False):
        """
        """
        if not debug:
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

    def get_neo4j_id(self, node="i:INGREDIENT", in_list=None):
        """
            Args:
                node(str): string in Cypher node format
                    (i:INGREDIENT) etc
                in_list(list): list of raw ids to match nodes

            Returns:
                ids(list): list of neo4j id properties for nodes
        """

        node_var, label = f"{node}".split(':')

        query = f"""
            MATCH ({node})
            WHERE {node_var}.{label.lower()} IN {in_list}
            RETURN id({node_var})
        """

        return self.driver.run(query).to_series().to_list()

    def get_matching_recipes(self, main_ingredients, side_ingredients):
        """

            Args:
                main_ingredints(list[str]): list of main_ingredient raw_ids and names
                    ['7213&tomato'] etc
                side_ingredient(list[int]): list of side_ingredient raw_ids and names

            Returns:
                results(list[dict]): list of matching recipes that contain main and side
                    ingredients
        """

        main_ingredients = [int(i.split('&')[0]) for i in main_ingredients]
        main_ingredients = self.get_neo4j_id(in_list=main_ingredients)

        try:
            side_ingredients = [int(i.split('&')[0]) for i in side_ingredients]
            side_ingredients = self.get_neo4j_id(in_list=side_ingredients)
        except ValueError as e:  # no side_ingredients

            query = """
            MATCH path=(i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE)
            WITH r,
                collect(DISTINCT id(i)) AS ingredients,
                $main_ingredients AS main, // user input
            WHERE all(x IN main
                WHERE (x IN ingredients))
            WITH r.name as RecipeName, id(r) as ID
            ORDER BY size([x IN side WHERE (x) IN ingredients]) DESC, r.n_ingredients
            WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
            RETURN result[0..10]
            """

            params = {"main_ingredients": main_ingredients}

            return query, params
            # res = self.driver.run(query, params)

            # results = res.data()
            # # results = results[0]["result[0..10]"]
            # # results = json.dumps(results)
            # # results = {'data': results}

            # return results

        query = """
        MATCH 
        (i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE)
        WITH
        r, collect(DISTINCT id(i)) AS ingredients,
        $main_ingredients AS main, $side_ingredients AS side
        WHERE 1=1
        and all(x IN main WHERE (x IN ingredients))
        and any(x IN side WHERE (x IN ingredients))
        WITH r.name as RecipeName, r.recipe as ID
        ORDER BY size([x IN side WHERE x IN ingredients]) DESC, r.n_ingredients
        WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
        RETURN result[0..10]
        """

        params = {"main_ingredients": main_ingredients,
                  "side_ingredients": side_ingredients}

        res = self.driver.run(query, params)

        results = res.data()

        results = results[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def test_get_matching_recipes(self, main_ingredients, side_ingredients):
        """
        """
        # TODO: implement the query Q1
        # query = """
        #         """

        # recipeName
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

        results = results[0]["result[0..9]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_content_based_recipes(self, user_id, main_ingredients, side_ingredients):

        query = """
        //Q2_Content based filtering
        MATCH//Find recipes similar to recpies rated by user (ID) #2203 and get their ingredients.
        (u:USER{user:$user})-[:RATED]->(r:RECIPE)-[s:SIMILAR]->(r2:RECIPE)-[:CONTAINS]->(i:INGREDIENT)
        WITH //save user_id, user rated recipes ( r ) and recipes similar to ( r ) along with a list of their aggregate ingredients
        u,r,r2,collect(DISTINCT id(i)) AS ingredients,
        count(r2.recipe) AS recipeCount, s.sim_score AS score, $main_ingredients AS main, $side_ingredients AS side
        WHERE 1=1 //filter only for recipes containing ALL main & ANY of the side ingredients
        and all(x IN main WHERE (x IN ingredients)) //all main
        and any(x IN side WHERE (x IN ingredients)) //any side
        WITH //return user_id, user_name, recipe rated by user, recommended recipe, similarity score and ingredient list in recommended recipe and calc number of matching ingredients in each recpie (no_sideIngr)
        u.user as user_id, r2.name as RecipeName, r.recipe as ID1, r2.recipe AS ID, r.name AS Name,ingredients, size([x IN side WHERE x IN ingredients]) as No_SideIngr, score
        ORDER BY No_SideIngr DESC, score DESC
        WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
        RETURN result[0..10]
        """

        main_ingredients = [int(i.split('&')[0]) for i in main_ingredients]
        main_ingredients = self.get_neo4j_id(in_list=main_ingredients)

        side_ingredients = [int(i.split('&')[0]) for i in side_ingredients]
        side_ingredients = self.get_neo4j_id(in_list=side_ingredients)

        params = {"main_ingredients": main_ingredients,
                  "side_ingredients": side_ingredients,
                  "user": user_id}
        res = self.driver.run(query, params).data()

        results = res[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def test_get_content_based_recipes(self, user_id, main_ingredients, side_ingredients):

        query = """
        //Q2_Content based filtering
        MATCH//Find recipes similar to recpies rated by user (ID) #2203 and get their ingredients.
        (u:USER{user:2203})-[:RATED]->(r:RECIPE)-[s:SIMILAR]->(r2:RECIPE)-[:CONTAINS]->(i:INGREDIENT)
        WITH//save user_id, user rated recipes ( r ) and recipes similar to ( r ) along with a list of their aggregate ingredients
        u,r,r2,collect(DISTINCT i.ingredient) AS ingredients, count(r2.recipe) AS recipeCount,
        s.sim_score AS score, [7213, 3184] AS main, [1170, 382, 5006] AS side
        WHERE 1=1 //filter only for recipes containing ALL main & ANY of the side ingredients
        and all(x IN main WHERE (x IN ingredients)) //all main
        and any(x IN side WHERE (x IN ingredients)) //any side
        WITH //return user_id, user_name, recipe rated by user, recommended recipe, similarity score and ingredient list in recommended recipe and calc number of matching ingredients in each recpie (no_sideIngr)
        u.user as user_id, r2.name as RecipeName, r.recipe as ID1, r2.recipe AS ID, r.name AS Name,ingredients, size([x IN side WHERE x IN ingredients]) as No_SideIngr, score
        ORDER BY No_SideIngr DESC, score DESC
        WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
        RETURN result[0..10]
                """

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

        results = results[0]["result[0..9]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_collaborative_recipes(self, user_id, main_ingredients, side_ingredients):
        # TODO: implement the query Q3

        query = """
            //Q3_Collaborative filter
            MATCH (r:RECIPE)<-[:RATED]-(u2:USER)<-[s:SIMILAR]-(u:USER {user:$user}) 
            WITH r, count(r.recipe) AS recipeCount, s.sim_score AS score 
            ORDER BY recipeCount DESC, score DESC 
            WITH (r) MATCH (r)-[:CONTAINS]->(i:INGREDIENT) 
            WITH r, collect(DISTINCT id(i)) AS ingredients,
            $main_ingredients AS main, $side_ingredients AS side MATCH (r) 
            WHERE 1=1 
                and all(x IN main WHERE (x IN ingredients)) 
                and any(x IN side WHERE (x IN ingredients)) 
            WITH r.recipe AS ID, r.name AS RecipeName, size([x IN side WHERE x IN ingredients]) as No_SideIngr 
            ORDER BY No_SideIngr DESC LIMIT 10
            WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
            RETURN result[0..10]
                """

        main_ingredients = [int(i.split('&')[0]) for i in main_ingredients]
        main_ingredients = self.get_neo4j_id(in_list=main_ingredients)

        side_ingredients = [int(i.split('&')[0]) for i in side_ingredients]
        side_ingredients = self.get_neo4j_id(in_list=side_ingredients)

        params = {"main_ingredients": main_ingredients,
                  "side_ingredients": side_ingredients,
                  "user": user_id}
        res = self.driver.run(query, params).data()

        results = res[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}
        return results

    def test_get_collaborative_recipes(self, user_id, main_ingredients, side_ingredients):
        # TODO: implement the query Q3
        # query = """
        #         """
        # results = self.driver.run(query).to_data_frame()
        # results = json.dumps(driver.run(query).data())

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

        results = results[0]["result[0..9]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_additional_ingredients(self, main_ingredients, side_ingredients):
        """
            Probable Ingredients
        """
        ingredients = main_ingredients.extend(side_ingredients)
        side_ingredients = [int(i.split('&')[0]) for i in ingredients]
        ingredients = self.get_neo4j_id(in_list=ingredients)

        query = """
                //Q4_Probable_ingredient
                WITH $ingredients AS ingredients	// Ingredient input list
                MATCH (r:RECIPE)		// only match recipes (r) that have relationships to ingredients input
                WHERE all(i in ingredients 
                WHERE EXISTS((r)-[:CONTAINS]->(:INGREDIENT {ingredient:i})))	// MATCH all relationships from the matched recipe node
                MATCH p=(r)-[relation:CONTAINS]->(i)	// aggregate by counting the relationships to paired ingredients from input
                WHERE NOT i.ingredient IN ingredients
                WITH count(relation) AS ingrCount, i
                ORDER BY ingrCount DESC
                WITH collect({ingredientName:i.name, ingredientID:i.ingredient}) AS res	// count how many times an ingredient appears in recipes
                RETURN res[0..9] // return all ingredients besides salt and tumeric, this needs to be fixed with another WHERE clause
                """

        params = {"ingredients": ingredients}
        res = self.driver.run(query, params).data()

        results = res[0]["result[0..10]"]
        results = json.dumps(results)
        results = {'data': results}
        return results

    def test_get_additional_ingredients(self, main_ingredients, side_ingredients):
        # TODO: implement the query Q4
        results = side_ingredients
        # query = """
        #         """
        # results = self.driver.run(query).to_data_frame()

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

        results = results[0]["res[0..9]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_relevant_ingredients(self, recipe_id):
        """
        """

        query = """
                //Q5_Ingredients in a recipe
                MATCH (i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE)
                WHERE r.recipe = $recipe_id
                RETURN i.name as ingredientName, i.ingredient as ingredientID
                """

        params = {"recipe_id": recipe_id}
        res = self.driver.run(query, params).data()

        results = res[0]
        results = json.dumps(results)
        results = {'data': results}
        return results

    def get_relevant_ingredients(self, recipe_id):
        # TODO: implement the query Q5
        # query = """
        #         """
        # results = self.driver.run(query).to_data_frame()
        # results = json.dumps(driver.run(query).data())

        results = [
            {
                "ingredientName": "basil",
                "ingredientID": 382
            },
            {
                "ingredientName": "parmesan cheese",
                "ingredientID": 5180
            },
            {
                "ingredientName": "red wine vinegar",
                "ingredientID": 6009
            },
            {
                "ingredientName": "olive oil",
                "ingredientID": 5006
            },
            {
                "ingredientName": "garlic",
                "ingredientID": 3184
            },
            {
                "ingredientName": "frozen pea",
                "ingredientID": 3046
            },
            {
                "ingredientName": "tomato",
                "ingredientID": 7213
            }
        ]

        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_alternative_ingredients(self, recipe_id):
        # TODO: implement the query Q8
        # query = """
        #         """
        # results = self.driver.run(query).to_data_frame()
        # results = json.dumps(driver.run(query).data())

        results = [
            {
                "ingredientName": "basil",
                "ingredientID": 382,
            },
            {
                "ingredientName": "parmesan cheese",
                "ingredientID": 5180
            },
            {
                "ingredientName": "red wine vinegar",
                "ingredientID": 6009
            }
        ]

        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_relevant_ratings(self, user_id, recipe_id):
        """

        """

        query = """//07_Recipe ratings
                MATCH (r:RECIPE)<-[o:RATED]-(u:USER)
                WITH r, u.user as user, o.rating AS rating
                WHERE r.recipe=$recipe+id
                WITH collect({ userID:user, rating:rating }) AS result
                RETURN result[0..10]
                """

        params = {"recipe_id": recipe_id, "user_id": user_id}
        res = self.driver.run(query, params).data()

        results = res[0]['0..10']
        results = json.dumps(results)
        results = {'data': results}
        return results

    def get_relevant_ratings(self, user_id, recipe_id):
        # TODO: implement the query Q7
        # query = """
        #         """
        # results = self.driver.run(query).to_data_frame()
        # results = json.dumps(driver.run(query).data())

        results = [
            {
                "result[0..9]": [
                    {
                        "rating": "5.0",
                        "userID": 4407
                    },
                    {
                        "rating": "5.0",
                        "userID": 4760
                    },
                    {
                        "rating": "5.0",
                        "userID": 10
                    },
                    {
                        "rating": "0.0",
                        "userID": 317
                    },
                    {
                        "rating": "5.0",
                        "userID": 325
                    },
                    {
                        "rating": "5.0",
                        "userID": 358
                    },
                    {
                        "rating": "4.0",
                        "userID": 395
                    },
                    {
                        "rating": "4.0",
                        "userID": 8321
                    },
                    {
                        "rating": "5.0",
                        "userID": 5132
                    }
                ]
            }
        ]

        results = results[0]["result[0..9]"]
        results = json.dumps(results)
        results = {'data': results}

        return results

    def get_recipe_details(self, recipe_id):
        # TODO: implement the query Q6
        query = """
                //Q6_Recipe_details
                MATCH (u:USER)-[o:RATED]->(r:RECIPE)
                WHERE r.recipe = 108091
                RETURN DISTINCT r.steps as steps, 
                r.calorie_level as calorieLevel, 
                r.n_ingredients as numberOfIngredients, 
                r.nutrition_dict as nutritionDetials, 
                r.tags as tags, 
                round(avg(tointeger(o.rating)),2) as avgRating, 
                count(o.rating) as numberOfRatings
                """

        results = json.dumps(self.driver.run(query).data())
        return results

    def test_get_recipe_details(self, recipe_id):

        results = [
            {
                "steps": "['heat oven to 350 degrees', 'brush the garlic cloves with 1 teaspoon of the oil , reserving the remaining oil', 'roast the oiled garlic cloves in a pan until golden and soft , about 10 to 15 minutes', 'watch carefully so garlic does not get over-brown or burn', 'carefully remove pan from oven and cool', 'when cool enough to handle , squeeze out the garlic pulp', 'combine the pulp with the reserved olive oil and rest of the ingredients in a blender', 'blend until smooth and use the dressing on any mixed garden salad', 'refrigerate leftover']",
                "calorieLevel": "2",
                "numberOfIngredients": 7,
                "nutritionDetials": "{'calories': 587.2, 'total fat': 84.0, 'sugar': 35.0, 'sodium': 1.0, 'protein': 9.0, 'saturated fat': 38.0, 'carbohydrates': 7.0}",
                "tags": "['30-minutes-or-less', 'time-to-make', 'course', 'main-ingredient', 'cuisine', 'preparation', 'occasion', 'north-american', 'low-protein', 'healthy', 'salads', 'fruit', 'vegetables', 'canadian', 'oven', 'refrigerator', 'dinner-party', 'holiday-event', 'picnic', 'salad-dressings', 'food-processor-blender', 'dietary', 'low-sodium', 'low-cholesterol', 'low-carb', 'healthy-2', 'ontario', 'low-in-something', 'citrus', 'lemon', 'onions', 'tomatoes', 'to-go', 'equipment', 'small-appliance', 'presentation', 'served-cold']",
                "avgRating": 4.46,
                "numberOfRatings": 13
            }
        ]

        results = json.dumps(results)
        results = {'data': results}

        return results
