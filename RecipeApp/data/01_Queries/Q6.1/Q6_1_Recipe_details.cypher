//Q6.1_Recipe_details
MATCH (u:USER)-[o:RATED]->(r:RECIPE)
WHERE r.recipe = 188315
RETURN round(avg(tointeger(o.rating)),2) as avgRating, count(o.rating) as numberOfRatings