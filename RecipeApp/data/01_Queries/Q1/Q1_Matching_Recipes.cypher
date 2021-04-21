//Q1_Matching Recipes
MATCH 
    (i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE)
WITH
    r, collect(DISTINCT id(i)) AS ingredients,
    [226, 4246] AS main, [28, 173, 4341] AS side
WHERE 1=1
    and all(x IN main WHERE (x IN ingredients))
    and any(x IN side WHERE (x IN ingredients))
WITH r.name as RecipeName, r.recipe as ID
ORDER BY size([x IN side WHERE x IN ingredients]) DESC, r.n_ingredients
WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
RETURN result[0..10]
