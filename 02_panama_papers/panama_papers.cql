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

// Highest numbers of entity for a same address
MATCH (a:Address)<-[REGISTERED_ADDRESS]-(e:Entity),
(a)-[:IS_IN_COUNTRY]->(c:Country)
WITH a,c, COUNT(e) AS nb_entity
WHERE nb_entity > 1
RETURN a.description, c.code, c.name, nb_entity
ORDER BY nb_entity DESC;

// Most concerned countries (Entities)
MATCH (e:Entity)-[:IS_IN_COUNTRY]->(co:Country)
RETURN co.name, COUNT(e) AS nb_entities
ORDER BY nb_entities DESC
LIMIT 50;

// Most concerned countries (Officers)
MATCH (o:Officer)-[:IS_IN_COUNTRY]->(co:Country)
WHERE co.code <> 'XXX'
RETURN co.name, COUNT(o) AS nb_officers
ORDER BY nb_officers DESC
LIMIT 50;

// Most concerned countries (Intermediaries)
MATCH (i:Intermediary)-[:IS_IN_COUNTRY]->(co:Country)
WHERE co.code <> 'XXX'
RETURN co.name, COUNT(i) AS nb_intermediaries
ORDER BY nb_intermediaries DESC
LIMIT 50;

// Most concerned countries
MATCH (c:Country)<-[:IS_IN_COUNTRY]-(n)
WHERE c.code <> 'XXX'
RETURN c.name, COUNT(n) AS nb_links
ORDER BY nb_links DESC;

// Entites country for french officers
MATCH (o:Officer)-[r]-(e:Entity),
      (o)-[:IS_IN_COUNTRY]->(c_o:Country),
      (e)-[:IS_IN_COUNTRY]->(c_r:Country)
WHERE c_o.name = 'France'
RETURN c_r.name, COUNT(e) AS nb_entities
ORDER BY nb_entities DESC;

// Most concerned countries
MATCH (c:Country)<-[:IS_IN_COUNTRY]-(n)
WHERE c.code <> 'XXX'
WITH c, n, COUNT(n) AS nb_links
RETURN c.name, nb_links, labels(n), COUNT(n)
ORDER BY nb_links DESC
LIMIT 50;