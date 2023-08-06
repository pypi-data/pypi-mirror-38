match paths = (p:Person {{name: '{name}'}})-[r:KNOWS]-(s:Person)
with paths
return nodes(paths)[0].name as person, collect(nodes(paths)[1].name) as friends
order by person
