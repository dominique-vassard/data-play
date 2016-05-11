/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                           IMPORT                                                                            //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//Create constaints
CREATE CONSTRAINT ON (d:Department) ASSERT d.name IS UNIQUE;
CREATE CONSTRAINT ON (t:Town) ASSERT t.name IS UNIQUE;
CREATE CONSTRAINT ON (s:Station) ASSERT s.name IS UNIQUE;
CREATE CONSTRAINT ON (di:District) ASSERT d.name IS UNIQUE;

// Import ata from CSV
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:/velib_a_paris_et_communes_limitrophes.csv' AS line FIELDTERMINATOR ';'
WITH line
MERGE(d:Department {name:line.dept})
MERGE (t:Town {name:line.ville})
MERGE (d)<-[:IS_IN_DEPT]-(t)
CREATE(s:Station {uuid:toInt(line.number), adress:line.address,name: line.name, latitude:toFloat(line.latitude), longitude:toFloat(line.longitude)})

//Managing Paris districts
FOREACH ( x IN (CASE WHEN line.dept = '75' THEN [1] ELSE [] END) |
    MERGE (di:District {name: toInt(substring(line.cp, 3))})-[:IS_IN_TOWN]->(t)
    MERGE (s)-[:IS_IN_DISTRICT]->(di)
)

//Managing non-districted towns
FOREACH ( y IN (CASE WHEN line.dept = '75' THEN [] ELSE [1] END) |
    MERGE (s)-[:IS_IN_TOWN]->(t)
)
;

//Result
//Nodes created: 1284
//Relationships created: 1280
//Properties set: 6200
//Labels added: 1284



/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                           PLAY!!                                                                            //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//All station in 13th district
MATCH (s:Station)-[r:IS_IN_DISTRICT]->(di:District {name:13}) RETURN s,r,di;

//Distance between 2 stations
MATCH (s:Station {uuid:13035}), (s2:Station {uuid:13008}) RETURN distance(point(s), point(s2));

//Get distance from all stations in the same district
MATCH (s:Station {uuid:13008})-[:IS_IN_DISTRICT]->(di:District)
(di)<-[:IS_IN_DISTRICT]-(s2:Station)
WITH s, s2, distance(point(s), point(s2)) AS distance_velib
RETURN s.uuid, s.name, s2.uuid, s2.name, distance_velib
ORDER BY distance_velib;

//Get greatest distance between two closes stations
MATCH (s:Station), (s2:Station)
WHERE s.uuid <> s2.uuid
WITH s, s2, distance(point(s), point(s2)) AS distance_velib
WITH s, MIN(distance_velib) AS min_dist
MATCH (s3:Station)
WHERE distance(point(s), point(s3)) = min_dist
RETURN s.uuid, s.name, s3.uuid, s3.name, min_dist
ORDER BY min_dist DESC
LIMIT 1;