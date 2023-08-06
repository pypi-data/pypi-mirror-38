MATCH (suggestion:Person)
WITH suggestion, size(()-[:KNOWS]-(suggestion)) as suggestion_friendships_count
match paths = (person:Person)-[:KNOWS *2..]-(suggestion)
where not (person)-[:KNOWS]-(suggestion) and person <> suggestion
with person, suggestion, suggestion_friendships_count, min(size(relationships(paths))) as suggestion_distance
merge (person)-[r:SHOULD_KNOWS]-(suggestion)
on create set r = {suggestion_friendships_count: suggestion_friendships_count, suggestion_distance:suggestion_distance}
on match set r = {suggestion_friendships_count: suggestion_friendships_count, suggestion_distance:suggestion_distance}
