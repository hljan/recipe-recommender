# from .graph_fixture import PyNeoGraphUI, RecipeQuery


# def test_run_q1(neo4j_driver):
#     recipe_q = RecipeQuery(neo4j_driver)
#     query = recipe_q.get_file(recipe_q.query_paths[0])

#     results = neo4j_driver.driver.run(query).data()
#     assert len(results[0]['result[0..10]']) == 10


# def test_q2(neo4j_driver):
#     recipe_q = RecipeQuery(neo4j_driver)
#     query = recipe_q.get_file(recipe_q.query_paths[1])
#     res = neo4j_driver.driver.run(query)
#     data = res.data()
#     result = data[0]['result[0..10]']
#     # assert len(result) == 10
#     assert len(result) == 2


# def test_q3(neo4j_driver):
#     recipe_q = RecipeQuery(neo4j_driver)
#     query = recipe_q.get_file(recipe_q.query_paths[2])
#     res = neo4j_driver.driver.run(query)
#     data = res.data()

#     result = data[0]['result[0..10]']
#     assert len(result) == 10


# def test_q4(neo4j_driver):
#     recipe_q = RecipeQuery(neo4j_driver)
#     query = recipe_q.get_file(recipe_q.query_paths[3])
#     res = neo4j_driver.driver.run(query)
#     data = res.data()

#     result = data[0]['result[0..10]']
#     assert len(result) == 10


# def test_q5(neo4j_driver):
#     recipe_q = RecipeQuery(neo4j_driver)
#     query = recipe_q.get_file(recipe_q.query_paths[4])
#     res = neo4j_driver.driver.run(query)
#     data = res.data()

#     assert data[0].keys() is not None
#     assert ['ingredientName', 'ingredientID'] == [i for i in data[0].keys()]


# def test_q6(neo4j_driver):
#     recipe_q = RecipeQuery(neo4j_driver)
#     query = recipe_q.get_file(recipe_q.query_paths[5])
#     res = neo4j_driver.driver.run(query)
#     data = res.data()
#     result = data[0]

#     assert ['steps', 'calorieLevel',
#             'numberOfIngredients', 'nutritionDetials',
#             'tags', 'avgRating', 'numberOfRatings'] == [i for i in result.keys()]


# def test_q7(neo4j_driver):
#     recipe_q = RecipeQuery(neo4j_driver)
#     query = recipe_q.get_file(recipe_q.query_paths[6])
#     res = neo4j_driver.driver.run(query)
#     data = res.data()

#     result = data[0]['result[0..10]']
#     assert len(result) == 10
