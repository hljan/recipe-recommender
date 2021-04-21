//Q6_Recipe_details
MATCH (u:USER)-[o:RATED]->(r:RECIPE)
WHERE r.recipe = 108091
RETURN DISTINCT r.steps as steps, r.calorie_level as calorieLevel, r.n_ingredients as numberOfIngredients, r.nutrition_dict as nutritionDetials, r.tags as tags, round(avg(tointeger(o.rating)),2) as avgRating, count(o.rating) as numberOfRatings