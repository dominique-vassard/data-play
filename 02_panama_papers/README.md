#Panama papers data play
If you don't know what are the Panama Papers, you probably live in a cave or while and it's time to get out. And get information [here](https://panamapapers.icij.org/#_ga=1.69803349.473767668.1463229349)  
On Monday, the 9th of May, the ICIJ releases the Panama Papers database. As ICIJ uses Neo4j as database and Linkurious as vizualisation tool, it isn't a surprise that the released data was in a graph DB friendly format.

First, we need the data.
You can get them from [here](https://offshoreleaks.icij.org/pages/database).  
If you are too lazy to click a link, you can download using this [official torrent](https://cloudfront-files-1.publicintegrity.org/offshoreleaks/data-csv.zip.torrent#_ga=1.131200970.473767668.1463229349).   

TL;DR? Too lazy to download data and convert them? Just want to perform a simple import? Just unzip the *clean_data/clean_data.zip* and jump to the [Import now!](#import-now) section

And if you're very lazy and/or want to perform a simple import, just read further.

First, have a look to the data

## The data
There are 4 csv files:

- *all_edges.csv* contains all relationships between nodes
- *Addresses.csv* contains all addresses
- *Entities.csv* contains entities information
- *Intermediaries.csv* contains all intermediaries (who can also be Officer, this point will be discucced later)
- *Officers.csv* contains all officers (who can also be Intermediary)

A little bit of vocabulary from the ICIJ:

*Offshore Entity:* A company, trust or fund created in a low-tax, offshore jurisdiction by an agent.  
*Agent (registered agent or offshore service provider):* Firm that provides services in an offshore jurisdiction to incorporate, register and manage an offshore entity at the request of a client.  
*Officer:* A person or company who plays a role in an offshore entity.  
*Intermediary:* A go-between for someone seeking an offshore corporation and an offshore service provider -- usually a law-firm or a middleman that asks an offshore service provider to create an offshore firm for a client.  
*Address:* Contact postal address as it appears in the original databases obtained by ICIJ.

Let's have a deeper look
###### all_edges.csv
Will be used to create (almost) all relationships  

field | description | note
---|---|---
node_1 | The source node | related to node_id fields in other files
rel_type | The relationship type | in lower case with spaces. Can countain special characters
node_2 | The target node | related to node_id fields in other files
  

###### Addresses.csv
Will be used to create **Address** nodes linked to:
- **Country**

field | description | note
---|---|---
address | The complete address
icij_id | An id used by the ICIJ | we won't use it
valid_until | Indicates the source of information (Offshore Leaks or Panama Papers) | we won't use it
country_codes | The address country codes | 3 letters, can be 'XXX'. separated by semi-colon. Will be used to create Country nodes 
countries | The address country names | can be 'Not identified'. separated by semi-colon
node_id | The node id | can be found in node_1 or node_2 field of all_edges.csv 
sourceID | Indicates the source of information (Offshore Leaks or Panama Papers) | we won't use it

###### Entities.csv
Will be used to create **Entity** nodes linked to:
- **Country**
- **Jurisdiction**
- **ServiceProvider**
- **EntityType**

field | description |note
---|---|---
name | The entity name | 
original_name | The entity original name | can be empty
former_name | The entity former name | can be empty
jurisdiction | The entity jurisdiction (country) | 3 letters, can be 'XXX'. Will be used to create Jurisdiction nodes
jurisdiction_description | The entity jurisdiction full name | can be 'undetermined'
company_type | The entity type | can be empty. Will be used to create EntityType nodes
address | The entity address
internal_id | An id used by ICIJ | we won't use it
incorporation_date | The date when an offshore entity was created
inactivation_date | The date when a client told the agent to deactivate the offshore entity, which could be reactivated at a later date
struck_off_date | A company becomes struck off when it fails to be in good standing, which happens when it fails to pay license fees. In the offshore world this is the equivalent to closing an entity, although it can be reactivated at a later date if the fees start being paid again
dorm_date | The date when an offshore entity stopped being active
status | The entity status
service_provider | The service provider name | Will be used to create ServiceProvider nodes
ibcRUC | The entity number | we won't use it
country_codes | The entity country codes | 3 letters, can be 'XXX'. separated by semi-colon. Will be used to create Country nodes
countries | The entity country names | can be 'Not identified'. separated by semi-colon
note | Additional note about the entity | can be empty
valid_until | Indicates the source of information (Offshore Leaks or Panama Papers) | we won't use it
node_id | The node id | can be found in node_1 or node_2 field of all_edges.csv 
sourceID | Indicates the source of information (Offshore Leaks or Panama Papers) | we won't use it

###### Intermediaries.csv
Will be used to create **Intermediary** nodes linked to:
- **Country**

field | description | note
---|---|---
name | The intermediary name
internal_id | An id used by ICIJ | we won't use it
address | The intermediary address | can be empty
valid_until | Indicates the source of information (Offshore Leaks or Panama Papers) | we won't use it
country_codes | The intermediary country codes | 3 letters, can be 'XXX'. separated by semi-colon. Will be used to create Country nodes
countries | The intermediary country names | can be 'Not identified'. separated by semi-colon
status | The intermediary status | can be empty 
node_id | The node id | can be found in node_1 or node_2 field of all_edges.csv  Can be duplicated in Officers.csv
sourceID | Indicates the source of information (Offshore Leaks or Panama Papers) | we won't use it

###### Officers.csv
Will be used to create **Officer** nodes linked to:
- **Country**

field | description | note
---|---|---
name | The Officer name
icij_id | An id used by ICIJ | we won't use it
valid_until | Indicates the source of information (Offshore Leaks or Panama Papers) | we won't use it
country_codes | The officer country codes | 3 letters, can be 'XXX'. separated by semi-colon. Will be used to create Country nodes
countries | The officer country names | can be 'Not identified'. separated by semi-colon
node_id | The node id | can be found in node_1 or node_2 field of all_edges.csv  Can be duplicated in Intermediaries.csv
sourceID | Indicates the source of information (Offshore Leaks or Panama Papers) | we won't use it


Don't hesitate to inspect the data, to know exactly what you're about to import. It's better to anticipate problem (format, incorrect data, etc.) before facing import fails.  
I inspected some of this data, you can check the `inspect_data.py` script if you're curious.

Now, we are all set. Let's import the data!

## Import
First, I wanted to import the data via `LOAD CSV` as the files are all csv.
It seems there is a problem with all_edges.csv: it isn't possible to dynamically create relationship type. A solution can be to use a `CASE` or even a `FOREACH` to force the relationship type. So, let's have a look on the different relationship in this file. Whoops, there is 121 kind of relationship.
Well, it seems that `LOAD CSV` is not a good idea...  
In fact, I imported all other files before seeing this problem. For information, I have to tweak the Java heap size and the queries (split, etc.) to perform import in almost satisyfing 20 minutes. Believe me, I was proud of these 20 minutes. But let's move on to the other solution: `neo4j-import`  

What is `neo4j-import`?  
The doc about this tool is [here](http://neo4j.com/docs/stable/import-tool.html)  
It's a tool to import data from CSV files into a blank database. Yep, a blank database and only a blak database, it will send an error if you try to use it on a non-empty database. Data sources are separated between nodes and relationships, each stored in CSV files. It is possible to specify a column to use as an Id and format other columns in a particular type if you want. In case of large file, you can have separated file for headers and data, which avoid to edit a large file only to change headers.  
It's a very quick introduction, I encourage you to read the [documentation](http://neo4j.com/docs/stable/import-tool.html) which is not that long.      

Knwowing how `neo4j-import` works, how can we import our data?
There are few things we ha to keep in mind about the data:
- There are duplicates between Officers and Intermediaries
- all_edges.rel_type is not suitable for database as they have special characters and spaces.  
Additionnally,extracting countries, jurisdictions, entity types and service providers to create nodes seems to be a good idea.  
Apart from the ICIJ-defined relationships (stored in all_edges.csv), we want the following meta graph:
![Schema](https://github.com/dominique-vassard/data-play/blob/master/02_panama_papers/images/meta_graph_import.png)

For data cleaning in file creating, I made a python script (my first python script, feel free to improve it and to help becoming better) which yau can call like this:  
`python convert_data_for_import.py sourceDirectory targetDirectory`  
with *sourceDirectory* the original files directory and *targetDirectory*, the directory where new files will be saved.  
Due to deduplication between **Officer** and **Intermediary**, the script run is a little bit long: around 6 minutes on my computer.

For convenience, the source from which data are retrieved will be noted as source_file.source_field. For example, an information stored in the field 'address' in the file Addresses.csv will be noted: Addresses.address.  
In file where *coutnry_codes* and *country_names* fields are present, there can be more than one country per line, separated by semi colon. The script split them in single country elements. 

It creates the following files:  
###### Addresses_headers.csv
Contains the header for the **Address** nodes file
Contains only one line:  
`uid:ID,description`  
The syntax `:ID` tells the import tool that data to use data in this colum as identifiers. It will use this identifiers when it comes to create relationships

###### Addresses.csv
Contains the **Address** nodes information

field | source | description
---|---|---
uid | Address.node_id | the node's unique identifier
description | Address.address | the address 

###### all_edges_headers.csv
Contains the headers for the ICIJ-defined relationships.  
Contains only one line:
`:START_ID,:END_ID,:TYPE`  
These are all keywords:
- `:START_ID` indicates a start node identifier. The import will look after the `:ID` set before to find the correct node  
- `:END_ID` indicates a target node identifier. The import will look after the `:ID` set before to find the correct node
- `:TYPE` is for the type of relationship to create

###### all_edges.csv
Contains all the headers for the ICIJ-defined relationships.  
These relationship are too numerous (121!) to be listed here. Eventually, you can use `CALL db.relationships()` to get all different kind of relationships. You can also see them in the browser's first tab.  

field | source | description
---|---|---
:START_ID | Addresses.node_id | A node's unique identifier
:END_ID | Addresses.country_codes | A node's unique identifier
:TYPE | - | The relationship's type


###### Countries_headers.csv
Contains the headers for the **Country** nodes.  
Contains only on line:  
`code:ID,name`

###### Countries.csv
Contains the **Country** nodes information.  
This information come from different files. 

field | source | description
---|---|---
code | Addresses.country_codes, Entities.country_codes, Officers.country_codes, Intermediaries.country_codes | the 3 letter country code. Will be use as identifier
name | Addresses.country_names, Entities.country_names, Officers.country_names, Intermediaries.country_names | The country name

###### Entities_headers.csv
Contains the headers for the **Entity** nodes.  
Contains only on line:  
`uid:ID,name,originalName,formerName,address,status,note,incorporationDate,dormancydate,inactivationDate,struckOffDate`

###### Entities.csv
Contains the **Entity** nodes information. 

field | source | description
---|---|---
uid | Entities.node_id | The **Entity** node unique identifier
name | Entities.name | The **Entity** name
originalName | Entities.original_name | The **Entity** original name
formerName | Entities.former_name | The **Entity** former name
address | Entities.address | The **Entity** address
status | Entities.status | The **Entity** status
note | Entities.note | Note about the **Entity** 
incorporationDate | Entities.incorporation_date | The **Entity** incorporation date
dormancydate | Entities.dorm_date | The **Entity** dormancy date
inactivationDate | Entities.inactivation_date | The **Entity** inactivation date
struckOffDate | Entities.struck_off_date | The **Entity** struck off date

###### EntityTypes_headers.csv
Contains the headers for the **EntityType** nodes.  
Contains only on line:  
`uid:ID,name`

###### EntityTypes.csv
Contains the **EntityType** nodes information. 

field | source | description
---|---|---
uid | - | The **EntityType** node unique identifier. Computed from each word first letter and type length
name | Entities.company_type | The **EntityType** description

###### Jurisdictions_headers.csv
Contains the headers for the **Jurisdiction** nodes.  
Contains only on line:  
`code:ID,name`

###### Jurisdictions.csv
Contains the **Jurisdiction** nodes information. 
Not to be confused with countries!  

field | source | description
---|---|---
uid | Entities.juridiction + Entities.jurisdiction length | The **Jurisdiction** node unique identifier.
name | Entities.jurisdiction | The **Jurisdiction** description

###### ServiceProviders_headers.csv
Contains the headers for the **ServiceProvider** nodes.  
Contains only on line:  
`uid:ID,name`

###### ServiceProviders.csv
Contains the **ServiceProvider** nodes information. 

field | source | description
---|---|---
uid | - | The **ServiceProvider** node unique identifier. Computed from each word first letter
name | Entities.service_provider | The **ServiceProvider** name 

###### additional_relationships_entity_headers.csv
Contains the headers for the relationships file between **Entity** nodes and **Jurisdiction** / **EntityType** / **ServiceProvider** nodes.  
Contains only one line:
`:START_ID,:END_ID,:TYPE`  
These are all keywords:
- `:START_ID` indicates a start node identifier, here an **Entity** one.  
- `:END_ID` indicates a target node identifier, here an **Jurisdiction** or **EntityType** or **ServiceProvider** one. 
- `:TYPE` is for the type of relationship to create

###### additional_relationships_entity.csv
field | source | description
---|---|---
:START_ID | Entities.node_id | An **Entity** node's unique identifier
:END_ID | Entities.jurisdiction | A **Jurisdiction** or **EntityType** or **ServiceProvider** node's unique identifier
:TYPE | - | The relationship's type. Here: *IS_IN_JURISDICTION* or *IS_OF_TYPE* or *HAS_SERVICE_PROVIDER* 

###### Intermediaries_headers.csv
Contains the headers for the **Intermediary** nodes.  
Contains only on line:  
`uid:ID,name,address,status`

###### Intermediaries.csv
Contains the **Intermediary** nodes information. 

field | source | description
---|---|---
uid | Intermediaries.node_id | The **Intermediary** node's unique identifier
name | Intermediaries.name | The **Intermediary** name
address | Intermediaries.address | The **Intermediary** address
status | Intermediaries.status | The **Intermediary** status

###### Officers_headers.csv
Contains the headers for the **Officer** nodes.  
Contains only on line:  
`uid:ID,name`

###### Officers.csv
Contains the **Officer** nodes information. 

field | source | description
---|---|---
uid | Officers.node_id | The **Officer** node's unique identifier
name | Officers.name | The **Officer** name

###### additional_relationships_country_headers.csv
Contains the headers for the relationships file between **Address** / **Entity** / **Intermediary** / **Officer** nodes and **Country** nodes.  
Contains only one line:
`:START_ID,:END_ID,:TYPE`  
These are all keywords:
- `:START_ID` indicates a start node identifier, here an **Address** / **Entity** / **Intermediary** / **Officer** one. 
- `:END_ID` indicates a target node identifier, here an **Country** one. 
- `:TYPE` is for the type of relationship to create

###### additional_relationships_country_officer.csv
Contains the relationships between **Address** / **Entity** / **Intermediary** / **Officer** nodes and **Country** ones. 

field | source | description
---|---|---
:START_ID | Addresses.node_id | An **Address** / **Entity** / **Intermediary** / **Officer** node's unique identifier
:END_ID | Addresses.country_codes | A **Country** node's unique identifier
:TYPE | - | The relationship's type. Here: *IS_IN_COUNTRY*

###### duplicateIds.csv
This file contains the duplicates between **Intermediary** and **Officer** nodes. If there is duplicated identifiers, the import tool can't create relationships because it can't know which one of the ndoes is the correct one to use for the purpose.  
This file structure is simple; jsut one header (`id`) and all identifiers. It will be used after the import

NOTA: It's possible to use less files by grouping relationships and nodes. But multiple files allow me to perform conversion tests and checks easily.

## Import now!
Now that we have all the required files, we can try to import the data in our database.  
Remember, `neo4j-import` only likes empty database, then we have to perform a:  
`rm -rf $PATH_TO_NEO4J/data/databases/graphdb/*`  
If you're running a Neo4j verion below 3, this command won't work. Check your graphdb to make it work, usually `rm -rf $PATH_TO_NEO4J/data/graphdb/*`  

And now, the import command:  
```shell
$PATH_TO_NEO4J/bin/neo4j-import --into $PATH_TO_NEO4J/data/databases/graph.db/ --multiline-fields=true \
--nodes:Address "/path/to/your/clean/data/Addresses_headers.csv,/path/to/your/clean/data/Addresses.csv" \
--nodes:Country "/path/to/your/clean/data/Countries_headers.csv,/path/to/your/clean/data/Countries.csv" \
--nodes:Entity "/path/to/your/clean/data/Entities_headers.csv,/path/to/your/clean/data/Entities.csv" \
--nodes:EntityType "/path/to/your/clean/data/EntityTypes_headers.csv,/path/to/your/clean/data/EntityTypes.csv" \
--nodes:Intermediary "/path/to/your/clean/data/Intermediaries_headers.csv,/path/to/your/clean/data/Intermediaries.csv" \
--nodes:Jurisdiction "/path/to/your/clean/data/Jurisdictions_headers.csv,/path/to/your/clean/data/Jurisdictions.csv" \
--nodes:Officer "/path/to/your/clean/data/Officers_headers.csv,/path/to/your/clean/data/Officers.csv" \
--nodes:ServiceProvider "/path/to/your/clean/data/ServiceProviders_headers.csv,/path/to/your/clean/data/ServiceProviders.csv" \
--relationships "/path/to/your/clean/data/additional_relationships_country_headers.csv,/path/to/your/clean/data/additional_relationships_country.csv" \
--relationships "/path/to/your/clean/data/additional_relationships_entity_headers.csv,/path/to/your/clean/data/additional_relationships_entity.csv" \
--relationships "/path/to/your/clean/data/all_edges_headers.csv,/path/to/your/clean/data/all_edges.csv"
```

That's a pretty big command, let's cut it into pieces!  
`$PATH_TO_NEO4J/bin/neo4j-import`  
calls the import tool  

`--into $PATH_TO_NEO4J/data/databases/graph.db/`  
tells the import tool where to import data  

`--multiline-fields=true`  
allows multiline value in fields  

`--nodes:Address "/path/to/your/clean/data/Addresses_headers.csv,/path/to/your/clean/data/Addresses.csv"`  
import data from */path/to/your/clean/data/Addresses.csv* using the headers stored in */path/to/your/clean/data/Addresses_headers.csv* and creates nodes of type **Address** with these data.  
The syntax is  
`--nodes:node_type "data_headers_file,datafile"`  
Beware: don't put sapces after the comma or the command will fail!
All other nodes types are imported the same way.  

For the relationship, the syntax is  
`--relationships "data_headers_file,datafile"`  
For example: `--relationships "/path/to/your/clean/data/all_edges_headers.csv,/path/to/your/clean/data/all_edges.csv"`


When you execute this command, it fails and you have this error:    
```
original error: At /home/dominique.vassard/Dev/perso/panama_papers/clean_data/Addresses.csv:124815 -  there's a field starting with a quote and whereas it ends that quote there seems to be characters in that field after that ending quote. That isn't supported. This is what I read: '11F.-2, No. 102, GUANGFU S. RD., XINYI DISTRICT, Taipei City 110, Taiwan, R.O.C "
```

Don't panic, it's just because this line ends with `\"` wich espaces the `"` and field is not delimited. Open the file, remove the `\` and execute thje command again.  

That's it! Everything was imported in our database.  
Remember the time required for my not-complete-LOAD-CSV import? About 20 minutes.  
How long was it for you? Far less I presume and your answers is in seconds. Nice, isn't it?  especially for more than 800,000 nodes and more than 3,000,000 relationships.

But our work isn't finished yet. We have to managed our duplicates. Some **Officer** nodes are also **Intermediary** ones, we stored wich one are concerned in a file. Let's import it:  
- First copy your *duplicateIds.csv* file into *$PATH_TO_NEO4J/import/*
- open your neo4-shell or your brower at localhost:7474
- Launch the query (about 1 min long)
```cypher
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM
'file:///panama_papers/duplicateIds.csv' AS line
WITH line
MATCH (n:Intermediary {uid: line.id})
SET n:Officer;
```
This query only get each **Intermediary** node with an identifier found in the file and to it the label **Officer**. These particular node will the be both **Intermediary** and **Officer** (you can query them with `:Intermediary:Officer`).  

Now our database has all the data, but to query it efficiently, it laks one thing: indexes. Open your shell or browser and let's add them. Remember that the browser accepts only one query at a time.
```cypher
CREATE INDEX ON :Country(code);
CREATE INDEX ON :Officer(name);
CREATE INDEX ON :Jurisdiction(code);
CREATE INDEX ON :EntityType(name);
CREATE INDEX ON :ServiceProvider(name);
CREATE INDEX ON :Entity(name);
CREATE INDEX ON :Address(description);
CREATE INDEX ON :Intermediary(name);
```


Now we're all good. We can launch the satisfying `CALL apoc.meta.graph()`, enjoy our metagraph:  
![Schema](https://github.com/dominique-vassard/data-play/blob/master/02_panama_papers/images/meta_graph.png)  

There's one thing you have to knwo about the tool import: you can specify field type by adding `:type_you_want` after the field name in the headers. But due to the `:ID` that indicates an identifier, it isn't possible to spcify types for identifier. Therefore, there are strings. Due to this,  
`MATCH (o:Officer {uid:12000001}) RETURN o.uid, o.name` won't work, but  
`MATCH (o:Officer {uid:'12000001'}) RETURN o.uid, o.name` will.
