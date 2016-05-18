/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                           IMPORT                                                                            //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Manage Officer and Intermediary duplicate
// Each duplicate will have both labels (Officer and Intermediary)
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM
'file:///panama_papers/duplicateIds.csv' AS line
WITH line
MATCH (n:Intermediary {uid: line.id})
SET n:Officer;

// Create indexes for best query performance
CREATE INDEX ON :Country(code);
CREATE INDEX ON :Officer(name);
CREATE INDEX ON :Jurisdiction(code);
CREATE INDEX ON :EntityType(name);
CREATE INDEX ON :ServiceProvider(name);
CREATE INDEX ON :Entity(name);
CREATE INDEX ON :Address(description);
CREATE INDEX ON :Intermediary(name);


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                           PLAY!!                                                                            //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Hihest numbers of entity for a same address
MATCH (a:Address)<-[REGISTERED_ADDRESS]-(e:Entity),
(a)-[:IS_IN_COUNTRY]->(c:Country)
WITH a,c, COUNT(e) AS nb_entity
WHERE nb_entity > 1
RETURN a.description, c.code, c.name, nb_entity
ORDER BY nb_entity DESC;