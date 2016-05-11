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


##A word on existing plays
###Velib Stations play (velib_station)
A play with velib statiob location.<br>
Velib is a self-service in Paris and its closest suburbs.<br>
We will extract all stations depending on district/department/town, closest station from a location, the minimum distance between two station of the set, etc.<br>