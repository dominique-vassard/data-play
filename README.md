#Data-play
A place to play and have fun with data

Various experiments on datasets with Neo4j (graph database)
In each directory, you will find:
  * a README.md wich explain what is done, from import to real play (with explanation about queries)
  * a CSV file, containing data to play with
  * a .cypher file containing all used queries

##Requirements
To play, you will need:
  * neo4j v3.x ([get it](http://neo4j.com/))
  * neo4j spatial procedures ([download and install infos](http://gist.asciidoctor.org/?dropbox-14493611%2Fcypher_spatial.adoc#_add_layer))
  * neo4j apoc procedures, which are must have ([download and install](https://github.com/neo4j-contrib/neo4j-apoc-procedures))<br>
This two sets of procedures requires [Maven](https://maven.apache.org/)<br>
And install can be long, you've been warned.<br>

## Resources
You can find documentation about Neo4j [here](http://neo4j.com/docs/developer-manual/current/)
You can find the very useful CYPHER cheatsheet [here](http://neo4j.com/docs/cypher-refcard/3.0/)
This two links can also be found in your browser ('Documentation' icon in the left panel)

##Ultra quick introduction to Neo4j
Neo4j is a graph database, from top to bottom. Every part of it, from storage to processing engine is designed for graph.

###But what is a graph?
A graph is just a set of node and relationship wich linked nodes with each other.
![What is a graph?](https://github.com/dominique-vassard/data-play/blob/master/images/whatisagraph.png)  
A node has at least one label, usually written in CamelCase.
A node can have properties (ex: name, location, etc.)
A relationship has one and only one type, usually written in uppercase.
A relationship can have properties.
Graph example:  
![Matrix](https://github.com/dominique-vassard/data-play/blob/master/images/graph_example.png)  
Here we have:
  * three nodes with the label *Human*
  * one node with the label *Ship*
  * on each *Human* node, a property called *name*
  * one relationship of type *BELIEVED_ID*
  * one relationship of type *OWNS*
  * one relationship of type *IS_CAPTAIN_OF*
  * one relationship of type *IS_CREW_OF*
  * one relationhip of type *BETRAYS* with a property called *when*

### Cypher
Cypher, apart from being a traitor, is also the language used to query the Neo4j graph database.  
It's a mixed between ASCII art and SQL.  
Nodes are represented like this: (:Label) 
And relationships like this: -[:TYPE]->  
Then if you want to get the human whom Morpheus believes in, you'll do:
```cypher
MATCH (m:Human)-[:BELIEVES_IN]->(n:Human)
WHERE m.name = "Morpheus"
RETURN n
```


This was an ultra quick introduction, check Neo4j documentation ofr more information.

##A word on existing plays
###Velib Stations play (velib_station)
A play with velib statiob location.<br>
Velib is a self-service in Paris and its closest suburbs.<br>
We will extract all stations depending on district/department/town, closest station from a location, the minimum distance between two station of the set, etc.<br>