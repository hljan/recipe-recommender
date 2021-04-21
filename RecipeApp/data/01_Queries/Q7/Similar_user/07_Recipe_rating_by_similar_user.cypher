//07_Recipe rating by similar user
MATCH (r:RECIPE)<-[o:RATED]-(u:USER)<-[s:SIMILAR]-(u2:USER {user:2203}) 
WITH r, u.user as user, o.rating AS rating, s.sim_score as score
WHERE r.recipe=108091
WITH collect({ userID:user, rating:rating, similarityScore:score }) AS result
RETURN result[0..9]