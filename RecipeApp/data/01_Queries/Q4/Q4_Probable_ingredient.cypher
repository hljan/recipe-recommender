//Q4_Probable_ingredient
WITH [7213, 3184] AS ingredients	// Ingredient input list
MATCH (r:RECIPE)		// only match recipes (r) that have relationships to ingredients input
WHERE all(i in ingredients 
WHERE EXISTS((r)-[:CONTAINS]->(:INGREDIENT {ingredient:i})))	// MATCH all relationships from the matched recipe node
MATCH p=(r)-[relation:CONTAINS]->(i)	// aggregate by counting the relationships to paired ingredients from input
WHERE NOT i.ingredient IN ingredients
WITH count(relation) AS ingrCount, i
ORDER BY ingrCount DESC
WITH collect({ingredientName:i.name, ingredientID:i.ingredient}) AS res	// count how many times an ingredient appears in recipes
RETURN res[0..10] // return all ingredients besides salt and tumeric, this needs to be fixed with another WHERE clause
