#Panama papers data play
If you don't know what are the Panama Papers, you probably live in a cave or while and it's time to get out. And get information [here](https://panamapapers.icij.org/#_ga=1.69803349.473767668.1463229349)  
On Monday, the 9th of May, the ICIJ releases the Panama Papers database. As ICIJ uses Neo4j as database and Linkurious as vizualisation tool, it isn't a surprise that the released data was in a graph DB friendly format.

First, we need the data.
You can get them from [here](https://offshoreleaks.icij.org/pages/database).  
If you are too lazy to click a link, you can download using this [official torrent](https://cloudfront-files-1.publicintegrity.org/offshoreleaks/data-csv.zip.torrent#_ga=1.131200970.473767668.1463229349).   
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


Now, we are all set. Let's import the data!

## Import
First, I wanted to import the data via `LOAD CSV` as the files are all csv.
It seems there is a problem with all_edges.csv: it isn't possible to dynamically create relationship type. A solution can be to use a `CASE` or even a `FOREACH` to force the relationship type. So, let's have a look on the different relationship in this file. Whoops, there is 121 kind of relationship.
Well, it seems that `LOAD CSV` is not a good idea...  
In fact, I imported all other files before seeing this problem. For information, I have to tweak the Java heap size and th queries to import in almost satisyfing 20 minutes. Believe me, I was proud of this 20 minutes. But let's move on to the other solution: `neo4j-import`  

What is `neo4j-import`?  
The doc about this tool is [here](http://neo4j.com/docs/stable/import-tool.html)  
It's a tool to import data from CSV files into a blank database. Yep, a blank database and only a blak database, it will send a nerror if you try to use it on a non-empty database. Data sources are separated between nodes and relationships, each stored in CSV files. It is possible to specify a column to use as an Id and format other columns in a particular type if you want. In case of large file, you can have separated file for headers and data, which avoid to edit a large file only to change headers.  
It's a very quick introduction, I encourage you to read the [doc](http://neo4j.com/docs/stable/import-tool.html).  

Knwowing how `neo4j-import` works, how can we import our data?
There are few things we ha to keep in mind about the data:
- There are duplicates between Officers and Intermediaries
- all_edges.rel_type is not suitable for database as they have special characters and spaces
Additionnally,extracting countries, jurisdictions, entity types and service providers to create nodes seems to be a good idea.
Apart from the ICIJ-defined relationships (stored in all_edges.csv), we want the following meta graph:


For data cleaning in file creating, I made a python script (my first python script, feel free to improve it and to help becoming better) which yau can call like this:  
`python convert_data_for_import.py sourceDirectory targetDirectory`
with *sourceDirectory* the original files directory and *targetDirectory*, the directory where new files will be saved.
It creates the following files:  
Addresses_headers.csv
Addresses.csv
additional_relationships_country_address_headers.csv
additional_relationships_country_address.csv
all_edges_headers.csv
all_edges.csv
Countries_headers.csv
Countries.csv
Entities_headers.csv
Entities.csv
EntityTypes_headers.csv
EntityTypes.csv
Jurisdictions_headers.csv
Jurisdictions.csv
ServiceProviders_headers.csv
ServiceProviders.csv
additional_relationships_entity_jurisdiction_headers.csv
additional_relationships_entity_jurisdiction.csv
additional_relationships_entity_headers.csv
additional_relationships_entity.csv
additional_relationships_country_entity_headers.csv
additional_relationships_country_entity.csv
Intermediaries_headers.csv
Intermediaries.csv
additional_relationships_country_intermediary_headers.csv
additional_relationships_country_intermediary.csv
Officers_headers.csv
Officers.csv
additional_relationships_country_officer_headers.csv
additional_relationships_country_officer.csv
duplicateIds.csv
  
```
original error: At /home/dominique.vassard/Dev/perso/panama_papers/clean_data/Addresses.csv:124815 -  there's a field starting with a quote and whereas it ends that quote there seems to be characters in that field after that ending quote. That isn't supported. This is what I read: '11F.-2, No. 102, GUANGFU S. RD., XINYI DISTRICT, Taipei City 110, Taiwan, R.O.C "
```