match paths = (p:Person {{name: '{name}'}})-[r:SHOULD_KNOWS]-(s:Person)
with paths
order by p.name, r.suggestion_distance asc, r.suggestion_friendships_count desc
return nodes(paths)[0].name as user, collect(nodes(paths)[1].name) as recommendations
order by user
