#                  ORIGINAL FILE FORMAT
#########################################################################################
# Officers.csv
# - name
# - icij_id
# - valid_until
# - country_codes
# - countries
# - node_id
# - sourceID
#
# Entities.csv
# - name
# - original_name
# - former_name
# - jurisdiction
# - jurisdiction_description
# - company_type
# - address
# - internal_id
# - incorporation_date
# - inactivation_date
# - struck_off_date
# - dorm_date
# - status
# - service_provider
# - ibcRUC
# - country_codes
# - countries
# - note
# - valid_until
# - node_id
# - sourceID
#
# Addresses.csv
# - address
# - icij_id
# - valid_until
# - country_codes
# - countries
# - node_id
# - sourceID
#
#
# Intermediaries.csv
#  - name
#  - internal_id
#  - address
#  - valid_until
#  - country_codes
#  - countries
#  - status
#  - node_id
#  - sourceID
#
#  all_edges.csv
#  - node_1
#  - rel_type
#  - node_2
#
#########################################################################################
#                      FINAL FILES FORMAT
#########################################################################################
#
# Officer_header.csv (contains Officer header information)
#   - uid:ID
#   - name
#
# Officer.csv (contains Officer Node info): has link to Country
#   - Officers.node_id
#   - Officers.name
#
# Country_header.csv (contains Country headers)
#   - code:ID
#   - name
#
# Country.csv (contains Country Node info)
#   - country_codes (split array)
#   - countries (split array)
#
# ServiceProvider_header (contains ServiceProvider headers)
#   - uid:ID
#   - name
#
# ServiceProvider.csv (contains ServiceProvider Node information)
#   - generated
#   - Entities.service_provider
#
# Jurisdiction_header.csv (contains Jurisdiction headers)
#   - code:ID
#   - name
#
# Jurisdiction.csv (contains Jurisdiction Node information)
#   - Entities.jurisdiction
#   - Entities.jurisdiction_description
#
# EntityType_header.csv (contains EntityType headers)
#   - uid:ID
#   - name
#
# EntityType.csv (contains EntityType information)
#   - generated
#   -Entities.company_type
#
# Entity_header.csv (contains Entity Node information)
#   - uid:ID
#   - name
#   - originalName
#   - formerName
#   - address
#   - status
#   - note
#   - incorporationDate
#   - dormancydate
#   - inactivationDate
#   - struckOffDate
#
# Entity.csv (contains Entity Node information): has link to Jurisdiction, Country, ServiceProvider, EntityType
#   - Entities.node_id
#   - Entities.name
#   - Entities.original_name
#   - Entities.former_name
#   - Entities.address
#   - Entities.status
#   - Entities.note
#   - Entities.incorporation_date
#   - Entities.dorm_date
#   - Entities.inactivation_date
#   - Entities.struck_off_date
#
# Address_header.csv (contains Address headers)
#   - uid:ID
#   - description
#
# Address.csv (contains Address Node information) : has link to Country
#   - Addresses.node_id
#   - Adresses.address
#
# Intermediary_header.csv (contains Intermediary headers)
#   - uid:ID
#   - name
#   - address
#   - status
#
# Intermediary.csv (contains Intermediary Node information): has link to Country
#   - Intermediaries.node_id
#   - Intermediaries.name
#   - Intermediaries.address
#   - Intermediaries.status
#
# relationships_headers (contains relationships headers)
#   - :START_ID,
#   - :END_ID,
#   - :TYPE
#
# relationships.csv (contains relationships)
#   - all_edges.node_1
#   - all_edges.node_2
#   - alledges.rel_type
#
# additional_relationships_headers.csv (contains additional relationships headers)
#   - :START_ID,
#   - :END_ID,
#   - :TYPE
#
# additional_relationships.csv (contains additional relationships)
# -> generated from previous files:
# (Officer)-[:IS_IN_COUNTRY]->(Country)
# (Entity)-[:IS_IN_COUNTRY]->(Country)
# (Entity)-[:IS_IN_JURISDICTION]->(Jurisdiction)
# (Entity)-[:IS_OF_TYPE]->(EntityType)
# (Entity)-[:HAS_SERVICE_PROVIDER]->(ServiceProvider)
# (Address)-[:IS_IN_COUNTRY]->(Country)
# (Intermediary)-[:IS_IN_COUNTRY]->(Country)


import sys
import converters
# import converters

sourceDirectory = sys.argv[1]
targetDirectory = sys.argv[2]

print "Reads file from " + sourceDirectory
print "Writes file into " + targetDirectory

countries = {}

# Convert/clean Intermediaries
resIntermediaries = converters.manageIntermediaries(sourceDirectory, targetDirectory, countries);
converters.addCountryRelationships(targetDirectory, resIntermediaries['relToCountry']);

# Convert/clean Officers
resOfficers = converters.manageOfficers(sourceDirectory, targetDirectory, countries, resIntermediaries['intermediariesId']);
converters.addCountryRelationships(targetDirectory, resOfficers['relToCountry']);

# Convert/clean Entities
resEntities = converters.manageEntities(sourceDirectory, targetDirectory, countries);
converters.addCountryRelationships(targetDirectory, resEntities['relToCountry']);

# Convert/clean Addresses
resAddresses = converters.manageAddresses(sourceDirectory, targetDirectory, countries);
converters.addCountryRelationships(targetDirectory, resAddresses['relToCountry']);

## Save Country nodes file
converters.saveCountries(targetDirectory, countries)

# Convert/Clean all_edges file
converters.manageAllEdges(sourceDirectory, targetDirectory)

