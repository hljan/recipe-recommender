//Q5_Ingredients in a recipe
MATCH (i:INGREDIENT)<-[:CONTAINS]-(r:RECIPE)
WHERE r.recipe = 41284
RETURN i.name as ingredientName, i.ingredient as ingredientID