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
SET n:Officer

// Create indexes for best query performance
CREATE INDEX ON :Country(code);
CREATE INDEX ON :Officer(name);
CREATE INDEX ON :Jurisdiction(code);
CREATE INDEX ON :EntityType(type);
CREATE INDEX ON :ServiceProvider(name);
CREATE INDEX ON :Entity(name);
CREATE INDEX ON :Address(description);
CREATE INDEX ON :Intermediary(name);


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                           PLAY!!                                                                            //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////