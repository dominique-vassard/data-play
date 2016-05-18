#Velib stations data play
Velib is a self-service bike system in Paris (France) and its closest suburbs.  
Bikes are available 24/7 in stations.  
More infos here [Velib](http://en.velib.paris.fr/)  
Stations geographic positions ae open data. So let's play!  

## About data in the file
The file contains a csv with the following fields:  
 
 Field name | Description                           | Our usage  
------------|---------------------------------------|-------------------------------------------------------------------------------------  
 number     | The station identifier                | uuid : unique node identifier  
 name       | The station name                      | name  
 address    | The station address                   | address  
 dept       | The station department                | Department  
 cp         | The station sip code                  | Used to kwnow wether the station belongs to an district (inside Paris) or not  
 ville      | The town where the station is located | Town  
 latitude   | The station latitude                  | latitude  
 longitude  | The station longitude                 | longitude  
 wgs84      | The station WGS84 coordinates (GPS)   | unused  

## Import data
Copy *velib_a_paris_et_communes_limitrophes.csv* to $NEO4J_PATH/import  
We use the data info file to create station nodes, district nodes, town nodes, department nodes and to link them  
At the end, our database schema will be like this:  
![Schema](https://github.com/dominique-vassard/data-play/blob/master/01_velib_stations/images/schema.png)  
We will see later how to generate this metagraph.


Now it's time to import the data.  
Start Neo4j if it's not already the case: $NEO4J_PATH/bin/neo4j start  
Now you've got two choices:
  * Use the browser at http://localhost/7474
  * Use the shell: $NEO4J_PATH/bin/neo4j-shell
Choice is all yours, depends if you prefer commande line and ruxtic table or pretty graph.  
Choose your weapon!


First, we create constraints
```cypher
CREATE CONSTRAINT ON (d:Department) ASSERT d.name IS UNIQUE;
CREATE CONSTRAINT ON (t:Town) ASSERT t.name IS UNIQUE;
CREATE CONSTRAINT ON (s:Station) ASSERT s.uuid IS UNIQUE;
CREATE CONSTRAINT ON (di:District) ASSERT d.name IS UNIQUE;
```
In order to make sure that uniqueness is preseve for our nodes.  
Constraints automatically create indexes on the constrained property.  
You can list existing constraints with `CALL db.constraints()` and indexes with `CALL db.indexes()`.


Here is the import query:
```cypher
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
);
```


Let's explain that a litlle bit!
```cypher
USING PERIODIC COMMIT
```
This permits to periodically commit as it says. But why is it useful?  
All transaction work is kept in memory before being committed. This means that without this instruction, all the nodes and relationships we create will be stored in memory until process successfully ends.  
So, be nice with your RAM and use this instruction.


```cypher
LOAD CSV WITH HEADERS FROM
'file:/velib_a_paris_et_communes_limitrophes.csv' AS line FIELDTERMINATOR ';'
WITH line
```
This instruction is pretty clear, just loading a CSV with semi-colon as field separator.  
`file:/` will look into your $NEO4J_PATH/import directory and only there.  
If you want to load a csv from the interwe, you can use `http://`  
Ad we will use the data line by line, that's the final line says.


```cypher
MERGE (d:Department {name:line.dept})
MERGE (t:Town {name:line.ville})
MERGE (d)<-[:IS_IN_DEPT]-(t)
```
Here we create our first nodes: Department and Town!  
Their names are from file data.  
`MERGE` uses the previoulsy created constraint and assure the the nodes uniqueness.  
the last `MERGE` links the created Town node to the Department node  
It is a good practice to have nodes label in CamelCase and the relationships type in upper case.


```cypher
CREATE(s:Station {uuid:toInt(line.number), adress:line.address,name: line.name, latitude:toFloat(line.latitude), longitude:toFloat(line.longitude)})
```
Creates the Station nodes.
All data we get from file are considered to be strings, then it's important to cast them in the right type if needed. Here we cast *longitude* and *latitude* to float to be able to perform specific operation on them.


```cypher
FOREACH ( x IN (CASE WHEN line.dept = '75' THEN [1] ELSE [] END) |
    MERGE (di:District {name: toInt(substring(line.cp, 3))})-[:IS_IN_TOWN]->(t)
    MERGE (s)-[:IS_IN_DISTRICT]->(di)
)
```
There's no `IF` in Cypher then here is the trick: use a `CASE` to fill an array either with a 1 (true) or keep it empty. Then iterate through this array via `FOREACH`.  
Not the easiest way to do a condition...  
With this pseudo-test, if the Station is located in Paris, we create the district if it doesn't exists (and link it to the town) and link the Station to the District.


```cypher
FOREACH ( y IN (CASE WHEN line.dept = '75' THEN [] ELSE [1] END) |
    MERGE (s)-[:IS_IN_TOWN]->(t)
)
```
As you've surely guessed, here is the opposite, we only link the Station to the Town.


And now (if you installed apoc procedures), you can visualize your meta-graph:
 ```cypher
CALL apoc.meta.graph();
 ```
Yep, this is cool!  
But now it's time to play!

## Play with data

#####What are the stations in the 13th district?
 ```cypher
MATCH (s:Station)-[r:IS_IN_DISTRICT]->(di:District {name:13}) 
RETURN s, r, di;
 ```

A pretty straight forward query, we get the *Station* linked to *District* whose name is '13' and return everything that was found.  
  
  
  
#####What is the distance between two given stations?
 ```cypher
MATCH (s:Station {uuid:13035}), (s2:Station {uuid:13008}) 
RETURN distance(point(s), point(s2));
 ```
Again, this is straight forward.  
`distance` use the nodes longitude and latitude to compute distance (in meters).
If these values aren't cast to float, `distance` doesn't work!  



#####What is the distance from one station to all aother station in the same district
```cypher
MATCH (s:Station {uuid:13008})-[:IS_IN_DISTRICT]->(di:District),
(di)<-[:IS_IN_DISTRICT]-(s2:Station)
RETURN s.uuid, s.name, s2.uuid, s2.name, distance(point(s), point(s2)) AS distance_velib
ORDER BY distance_velib;
```
Let' explain this one.  
`MATCH (s:Station {uuid:13008})-[:IS_IN_DISTRICT]->(di:District)`  
For the *Station* with *uuid* equals to 13008, we retrieve the district it's linked to (in a simpler way: we get the *Station*'s *District*).  
`(di)<-[:IS_IN_DISTRICT]-(s2:Station)`  
Given this *District* (aliased 'di'), we retrieve all *Station* it's linked to.    
Now that we have all *Station* in the same *District*, all we need to do is to compute the distance between the found *Station*s and the given one, which is done by:  
`RETURN s.uuid, s.name, s2.uuid, s2.name, distance(point(s), point(s2)) AS distance_velib`  
The results are then order using `ORDER BY`.  
We could add a `LIMIT` clause to get only the closest or the furthest *Station* depending on the `ORDER BY`.  



#####What is the greatest distance between two closest station?
Last but not least, an interesting question. We have our dataset with all stations and geo-coordinate and we want to know which closest have the greatest distance between them.  
It could be interesting to have this information if we wonder where it will be more useful to add a new station.  
Here is the query:  
```cypher
MATCH (s:Station), (s2:Station)
WHERE s.uuid < s2.uuid
WITH s, s2, distance(point(s), point(s2)) AS distance_velib
WITH s, MIN(distance_velib) AS min_dist
MATCH (s3:Station)
WHERE distance(point(s), point(s3)) = min_dist
RETURN s.uuid, s.name, s3.uuid, s3.name, min_dist
ORDER BY min_dist DESC
LIMIT 1;
```

This query is pretty long to run (depending on ypur computer, it could take from 30 to more 150 seconds). Nothing unexpected as we use all of our graph.  But I still need to find an optimized query.  

```cypher
MATCH (s:Station), (s2:Station)
WHERE s.uuid <> s2.uuid
```
First we build all the possible pairs of *Station*  
`WITH s, s2, distance(point(s), point(s2)) AS distance_velib`  
`WITH` is a very handy instruction that acts like: Use these data as start for the reste of the query. Here we'll get the two *Station* and the distance between them.  
`WITH s, MIN(distance_velib) AS min_dist`
And then only keep one of the *Station* and the mininum distance between this *Station* and the closest.  
Now we need to get the information about these closest *Station*, and here is how to get it:  
```cypher
MATCH (s3:Station)
WHERE distance(point(s), point(s3)) = min_dist
```

And now, we only have to return the result:
```cypher
RETURN s.uuid, s.name, s3.uuid, s3.name, min_dist
ORDER BY min_dist DESC
LIMIT 1;
```
And here it is, finally!
```
+-------------------------------------------------------------------------------------------------------+
| s.uuid | s.name                           | s3.uuid | s3.name                     | min_dist          |
+-------------------------------------------------------------------------------------------------------+
| 28002  | "28002 - SOLJENITSYNE (PUTEAUX)" | 28001   | "28001 - WALLACE (PUTEAUX)" | 803.5921865410247 |
+-------------------------------------------------------------------------------------------------------+
```