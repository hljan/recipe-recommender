//Q3_Collaborative filter
MATCH (r:RECIPE)<-[:RATED]-(u2:USER)<-[s:SIMILAR]-(u:USER {user:2203}) 
WITH r, count(r.recipe) AS recipeCount, s.sim_score AS score 
ORDER BY recipeCount DESC, score DESC 
WITH (r) MATCH (r)-[:CONTAINS]->(i:INGREDIENT) 
WITH r, collect(DISTINCT i.ingredient) AS ingredients,[7213, 3184] AS main, [1170, 382, 5006] AS side MATCH (r) 
WHERE 1=1 
    and all(x IN main WHERE (x IN ingredients)) 
    and any(x IN side WHERE (x IN ingredients)) 
WITH r.recipe AS ID, r.name AS RecipeName, size([x IN side WHERE x IN ingredients]) as No_SideIngr 
ORDER BY No_SideIngr DESC LIMIT 10
WITH collect({ recipeName:RecipeName, recipeID:ID }) AS result
RETURN result[0..9]