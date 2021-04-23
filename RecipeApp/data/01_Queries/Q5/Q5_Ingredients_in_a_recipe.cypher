//Q5_Ingredients in a recipe
MATCH (i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE), (a:INGREDIENT)<-[s:SIMILAR]-(i:INGREDIENT)
WHERE r.recipe = 41284
RETURN i.name as ingredientName, i.ingredient as ingredientID, collect(Distinct a.name) as alternateIngredient