//Q6_Recipe_details
MATCH (r:RECIPE)
WHERE r.recipe = 188315
RETURN DISTINCT r.steps as steps, r.n_ingredients as numberOfIngredients, r.nutrition_dict as nutritionDetials, r.tags as tags