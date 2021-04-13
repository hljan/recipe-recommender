//Q1 Match Recipes

MATCH (i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE)
WHERE id(i) IN [226, 28172, 173, 28267, 28]
RETURN id(r), r.name, r.n_ingredients, COUNT(*) AS occ
ORDER BY occ DESC, r.n_ingredients;

//Q2 Content Based Filtering

MATCH p=(u:USER{user:"2203"})-[:RATED]->(r:RECIPE)-[s:SIMILAR]->(r2:RECIPE)-[:CONTAINS]->(i:INGREDIENT)
WITH u, r, r2,
    collect(DISTINCT i.ingredient) AS ingredients,
    count(r2.recipe) AS recipeCount, s.sim_score AS score,
    ['1584','6906'] AS main,
    ['2499','840','6270','1609','1909','7449','1591'] AS side
WHERE all(x IN main WHERE (x IN ingredients))
    AND any(x IN side WHERE (x IN ingredients))
RETURN ingredients,
    r.recipe, r.name,
    r2.recipe, r2.name,
    toInteger(u.user),
    size([x IN side WHERE x IN ingredients]) AS No_SideIngr, score
    ORDER BY No_SideIngr DESC, score DESC

// Q3 Collaborative Based Filter

MATCH (r:RECIPE)<-[:RATED]-(u2:USER)<-[s:SIMILAR]-(u:USER {user:"2203"})
WITH r, count(r.recipe) AS recipeCount, s.sim_score AS score
ORDER BY recipeCount DESC, score DESC
WITH (r)
MATCH (r)-[:CONTAINS]->(i:INGREDIENT)
WITH r, collect(DISTINCT id(i)) AS ingredients
MATCH (r)
WHERE all(x IN [7565,8073] WHERE (x IN ingredients)) AND
    any(x IN [7565,8073] WHERE (x IN ingredients))
RETURN r.name LIMIT 3;


MATCH (r:RECIPE)<-[:RATED]-(u2:USER)<-[s:SIMILARITY]-(u:USER {user:"2203"}) //Find recipes rated by similar users of user#2203
WITH r, count(r.recipe) AS recipeCount, s.sim_score AS score //Store filtered recipes, number of recipes repeated in the result by similar user, similarity score between users
ORDER BY recipeCount DESC, score DESC //order recipes by recipeCount and similarity score

WITH (r)
MATCH (r)-[:CONTAINS]->(i:INGREDIENT) //With the selected recipes, find ingredients per recipe

WITH r, collect(DISTINCT i.ingredient) AS ingredients, //Store selected recipes, lists of ingredients, selected main ingredients, selected side ingredients
        ['1584','6906'] AS main, ['2499','840','6270','1609','1909','7449','1591'] AS side
MATCH (r) //Find recipes where all the main ingredients are included and any of the side ingredients are included
WHERE all(x IN main WHERE (x IN ingredients)) //cocoa, sugar
AND any(x IN side WHERE (x IN ingredients))  //egg, butter, salt, coconut oil, cream, vanilla, coconut
RETURN r.recipe AS ID, r.name AS Name, size([x IN side WHERE x IN ingredients]) as No_SideIngr //Return recipe IDs, names, number of side ingredients included in ingredient list
ORDER BY No_SideIngr DESC
LIMIT 10

// Q4 Most probable ingredients

WITH ["salt", "turmeric"] AS ingredients
MATCH (r:RECIPE)
WHERE all(i in ingredients
    WHERE EXISTS((r)-[:CONTAINS]->(:INGREDIENT {name:i})))
MATCH p=(r)-[relation:CONTAINS]->(i)
WHERE NOT i.name IN ingredients
WITH count(relation) AS ingrCount, i
ORDER BY ingrCount DESC
WITH collect({count:ingrCount, ingredients:i.name}) AS res
RETURN res[0..9]


