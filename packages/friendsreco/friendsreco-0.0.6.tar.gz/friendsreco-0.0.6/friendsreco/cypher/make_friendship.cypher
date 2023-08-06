MERGE (p:Person {{name: '{person}'}})
MERGE (f:Person {{name: '{friend}'}})
MERGE (p)-[:KNOWS]-(f)
RETURN (p)-[:KNOWS]-(f)
