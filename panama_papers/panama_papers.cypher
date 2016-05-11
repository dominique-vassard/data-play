/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                           IMPORT                                                                            //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//Create constaints
CREATE CONSTRAINT ON (c:Country) ASSERT c.code IS UNIQUE;
CREATE CONSTRAINT ON (o:Officer) ASSERT o.uuid IS UNIQUE;

//Import officers and link them to countries
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:/panama_papers/Officers.csv' AS line
WITH line
MERGE (c:Country {code:COALESCE(line.country_codes, 'XXX'), name: COALESCE(line.countries, 'Not identified')})
MERGE (o:Officer {uuid:line.node_id, name: COALESCE(line.name, 'Unknown')})
MERGE (o)-[:IS_OF_COUNTRY]->(c);
