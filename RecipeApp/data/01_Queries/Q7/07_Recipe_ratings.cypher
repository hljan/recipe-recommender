//07_Recipe ratings
MATCH (r:RECIPE)<-[o:RATED]-(u:USER)
WITH r, u.user as user, o.rating AS rating
WHERE r.recipe=108091
WITH collect({ userID:user, rating:rating }) AS result
RETURN result[0..9]