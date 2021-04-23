//Q1_Matching Recipes
MATCH 
    (i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE)
WITH
    r, collect(DISTINCT i.ingredient) AS ingredients,
    [7213, 3184] AS main, [1170, 382, 5006] AS side
WHERE 1=1
    and all(x IN main WHERE (x IN ingredients))
    and any(x IN side WHERE (x IN ingredients))
WITH r.name as RecipeName, r.recipe as ID
ORDER BY size([x IN side WHERE x IN ingredients]) DESC, r.n_ingredients
WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
RETURN result[0..9]