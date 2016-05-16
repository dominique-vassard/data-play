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


Now, we are all set. Let's import ALL the data!

## Import
Coming very soon (2 days max, but if you're curious enough, the files can talk)  