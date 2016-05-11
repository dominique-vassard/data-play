#Velib stations data play
Velib is a self-service bike system in Paris (France) and its closest suburbs.<br>
Bikes are available 24/7 in stations.<br>
More infos here [Velib](http://en.velib.paris.fr/)<br>
Stations geographic positions ae open data. So let's play!<br>

##Requirements
To play, you will need:
  * neo4j v3.x ([get it](http://neo4j.com/))
  * neo4j spatial procedures ([download and install infos](http://gist.asciidoctor.org/?dropbox-14493611%2Fcypher_spatial.adoc#_add_layer))
  * neo4j apoc procedures, which are some must have ([download and install](https://github.com/neo4j-contrib/neo4j-apoc-procedures))

## About data in the file
The file contains a csv with the following fields:<br>
 Field name | Description                           | Our usage<br>
------------|---------------------------------------|-------------------------------------------------------------------------------------<br>
 number     | The station identifier                | uuid : unique node identifier<br>
 name       | The station name                      | name<br>
 address    | The station address                   | address<br>
 dept       | The station department                | Department<br>
 cp         | The station sip code                  | Used to kwnow wether the station belongs to an district (inside Paris) or not<br>
 ville      | The town where the station is located | Town<br>
 latitude   | The station latitude                  | latitude<br>
 longitude  | The station longitude                 | longitude<br>
 wgs84      | The station WGS84 coordinates (GPS)   | unused<br>

## Import data
Copy velib_a_paris_et_communes_limitrophes.csv to $NEO4J_PATH/import<br>
We use the data info file to create station nodes, district nodes, town nodes, department nodes and to link them<br>
At the end, our database schema will be like this:<br>
![Schema](https://github.com/dominiquevas/data-play/blob/master/velib_stations/schema.png)<br>
We will see later how to generate this metagraph.

Now it's time to import the data.<br>
Start Neo4j if it's not already the case: $NEO4J_PATH/bin/neo4j start<br>
Now you've got two choices:
  * Use the browser at http://localhost/7474
  * Use the shell: $NEO4J_PATH/bin/neo4j-shell
Choice is all yours, depends if you prefer commande line and ruxtic table or pretty graph.<br>
Choose your weapon!


First, we create constraints
```cypher
CREATE CONSTRAINT ON (d:Department) ASSERT d.name IS UNIQUE;
CREATE CONSTRAINT ON (t:Town) ASSERT t.name IS UNIQUE;
CREATE CONSTRAINT ON (s:Station) ASSERT s.uuid IS UNIQUE;
CREATE CONSTRAINT ON (di:District) ASSERT d.name IS UNIQUE;
```
In order to make sure that uniqueness is preseve for our nodes.<br>
Constraints automatically create index on the constrained property.<br>
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
This permits to periodically commit as it says. But why is it useful.<br>
All transaction work is kept in memory before being committed. This means that without this instruction, all the nodes and relationships we create<br>
will be stored in memory until process successfully ends.<br>
So, be nice with your RAM and use this instruction.


```cypher
LOAD CSV WITH HEADERS FROM
'file:/velib_a_paris_et_communes_limitrophes.csv' AS line FIELDTERMINATOR ';'
WITH line
```
This instruction is pretty clear, just loading a CSV with semi-colon as field separator.<br>
`file:/` will look into your $NEO4J_PATH/import directory and only there.<br>
If you want to load a csv from the interwe, you can use `http://`<br>
Ad we will use the data line by line, that's the final line says.


```cypher
MERGE (d:Department {name:line.dept})
MERGE (t:Town {name:line.ville})
MERGE (d)<-[:IS_IN_DEPT]-(t)
```
Here we create our first nodes: Department and Town!<br>
Their names are from file data.<br>
`MERGE` uses the previoulsy created constraitn and assure the the nodes uniqueness.<br>
the last `MERGE` links the created Town node to the Department node<br>
It is a good practice to have nodes label in CamelCase and the relationships type in upper case.


```cypher
CREATE(s:Station {uuid:toInt(line.number), adress:line.address,name: line.name, latitude:toFloat(line.latitude), longitude:toFloat(line.longitude)})
```
Creates the Station nodes


```cypher
FOREACH ( x IN (CASE WHEN line.dept = '75' THEN [1] ELSE [] END) |
    MERGE (di:District {name: toInt(substring(line.cp, 3))})-[:IS_IN_TOWN]->(t)
    MERGE (s)-[:IS_IN_DISTRICT]->(di)
)
```
There's no `IF` in Cypher then here is the trick: use a `CASE` to fill an array either with a 1 (true) or keep it empty. Then iterate through this array via `FOREACH`.<br>
Not the easiest way to do a condition...<br>
With this pseudo-test, if the Station is located in Paris, we create the district if it doesn't exists (and link it to the town) an link the Station to the District.


```cypher
FOREACH ( y IN (CASE WHEN line.dept = '75' THEN [] ELSE [1] END) |
    MERGE (s)-[:IS_IN_TOWN]->(t)
)
```
As you've surely guess, here is the opposite, we only link the Station to the Town.


And now (if you installed apoc procedures), you can visualize your meta-graph:
 ```cypher
CALL apoc.meta.graph();
 ```