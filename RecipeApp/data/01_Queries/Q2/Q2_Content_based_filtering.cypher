//Q2_Content based filtering
MATCH//Find recipes similar to recpies rated by user (ID) #2203 and get their ingredients.
(u:USER{user:2203})-[:RATED]->(r:RECIPE)-[s:SIMILAR]->(r2:RECIPE)-[:CONTAINS]->(i:INGREDIENT)
WITH//save user_id, user rated recipes ( r ) and recipes similar to ( r ) along with a list of their aggregate ingredients
u,r,r2,collect(DISTINCT i.ingredient) AS ingredients, count(r2.recipe) AS recipeCount, s.sim_score AS score, [7213, 3184] AS main, [1170, 382, 5006] AS side
WHERE 1=1 //filter only for recipes containing ALL main & ANY of the side ingredients
and all(x IN main WHERE (x IN ingredients)) //all main
and any(x IN side WHERE (x IN ingredients)) //any side
WITH //return user_id, user_name, recipe rated by user, recommended recipe, similarity score and ingredient list in recommended recipe and calc number of matching ingredients in each recpie (no_sideIngr)
u.user as user_id, r2.name as RecipeName, r.recipe as ID1, r2.recipe AS ID, r.name AS Name,ingredients, size([x IN side WHERE x IN ingredients]) as No_SideIngr, score
ORDER BY No_SideIngr DESC, score DESC
WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
RETURN result[0..10]