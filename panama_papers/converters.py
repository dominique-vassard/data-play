import csv, os, re

######################################################################################################################
#                                                   OFFICERS                                                         #
######################################################################################################################
# It is possible to haveduplmicate between Officers and Intermediaries
def manageOfficers(sourceDir, targetDir, countries, intermediariesId):
    """Import and convert data from Officers.csv"""

    print "==========> Import and convert data from " + sourceDir + "Officers.csv to " + targetDir + "Officers.csv"

    #Write Officers headers file
    print "  * Create headers"
    with open(targetDir + 'Officers_headers.csv', 'wb') as headers:
        writer = csv.writer(headers, delimiter = ',')
        writer.writerow(["uid:ID", "name"])

    officerToCountry = {}

    duplicatesId = []

    #Manage Officers data
    print "  * Write file"
    with open(sourceDir + 'Officers.csv', 'rb') as source:
        reader = csv.DictReader(source, delimiter = ',')
        with open(targetDir + 'Officers.csv', 'wb') as target:
            writer = csv.writer(target, delimiter = ',')
            for row in reader:
                #Manage empty country info
                if row['country_codes'] == '':
                    row['country_codes'] = 'XXX'
                    row['countries'] = 'Not identified'

                #Countries can be an string separated by semi-colon
                countryCodeList = row['country_codes'].split( ';')
                countryNameList = row['countries'].split(';')
                for countryCode, countryName in zip(countryCodeList, countryNameList):
                    countries[countryCode] = countryName
                    officerToCountry[row['node_id']] = countryCode

                if (row['node_id'] in intermediariesId):
                    duplicatesId.append(row['node_id'])
                else:
                    writer.writerow([row['node_id'], row['name']])

    #Save duplicate id in a file
    with open(targetDir + 'duplicateIds.csv', 'wb') as duplicateFile:
        writer = csv.writer(duplicateFile, delimiter = ',')
        wrtier.writerow(['id'])
        for _, duplicateId in enumerate(duplicatesId):
            writer.writerow([duplicateId])

    return {'countries': countries, 'relToCountry': officerToCountry}

######################################################################################################################
#                                                   ENTITIES                                                         #
######################################################################################################################
def manageEntities(sourceDir, targetDir, countries):
    """Import and convert data from Officers.csv"""

    print "==========> Import and convert data from " + sourceDir + "Entities.csv to " + targetDir + "Entities.csv"


    #Write headers file
    headers = ['uid:ID', 'name', 'originalName', 'formerName', 'address', 'status', 'note', 'incorporationDate', 'dormancydate', 'inactivationDate', 'struckOffDate']
    writeHeaders(targetDir, 'Entities',                             headers)
    writeHeaders(targetDir, 'Jurisdictions',                        ['uid:ID', 'code', 'name'])
    writeHeaders(targetDir, 'ServiceProviders',                     ['code:ID', 'name'])
    writeHeaders(targetDir, 'EntityTypes',                          ['uid:ID', 'name'])
    writeHeaders(targetDir, 'additional_relationships_entity',      [':START_ID', ':END_ID', ':TYPE'])

    entityToCountry = {}

    additional_relationships = []

    jurisdictions = {}
    serviceProviders = {}
    entityTypes = {}

    print "  * Write file [Entities]"
    with open(sourceDir + 'Entities.csv', 'rb') as source:
        reader = csv.DictReader(source)
        with open(targetDir + 'Entities.csv', 'wb') as target:
            writerEntity = csv.writer(target)
            for row in reader:
                #Manage empty country info
                if row['country_codes'] == '':
                    row['country_codes'] = 'XXX'
                    row['countries'] = 'Not identified'

                #Countries can be an string separated by semi-colon
                countryCodeList = row['country_codes'].split( ';')
                countryNameList = row['countries'].split(';')
                for countryCode, countryName in zip(countryCodeList, countryNameList):
                    countries[countryCode] = countryName
                    entityToCountry[row['node_id']] = countryCode

                #Manage empty jurisdictions info
                if row['jurisdiction'] == '':
                    row['jurisdiction'] = 'XXX'
                    row['jurisdiction_description'] = 'Undetermined'

                #Manage jurisdictions
                jurId = 'jur-' + row['jurisdiction']
                jurisdictions[row['jurisdiction']] = row['jurisdiction_description']
                additional_relationships.append([row['node_id'], jurId, 'IS_IN_JURISDICTION'])

                #Manage empty serviceProvider info
                if row['service_provider'] == '':
                    spId = 'sp-XXX'
                    row['service_provider'] = 'Undetermined'
                else:
                    spId = ''
                    details = row['service_provider'].split()
                    for _, detail in enumerate(details):
                        spId += detail[:1]

                #Manage serviceProvider
                serviceProviders[spId] = row['service_provider']
                additional_relationships.append([row['node_id'], spId, 'HAS_SERVICE_PROVIDER'])

                #Manage empty entity type info
                if row['company_type'] == '':
                    typeId = 'et-XXX'
                    row['company_type'] = 'Undetermined'
                else:
                    typeId = ''
                    details = row['company_type'].split()
                    for _, detail in enumerate(details):
                        typeId += detail[:1] + str(len(detail))

                #Manage entityTypes
                entityTypes[typeId] = row['company_type']
                additional_relationships.append([row['node_id'], typeId, 'IS_OF_TYPE'])

                writerEntity.writerow([row['node_id'],
                                       row['name'],
                                        row['original_name'],
                                        row['former_name'],
                                        row['address'],
                                        row['status'],
                                        row['note'],
                                        row['incorporation_date'],
                                        row['dorm_date'],
                                        row['inactivation_date'],
                                        row['struck_off_date']])

    # Write jurisdictions file
    print "  * Write file [Jurisdictions]"
    with open(targetDir + 'Jurisdictions.csv', 'wb') as jurisdictionFile:
        writer = csv.writer(jurisdictionFile, delimiter = ',')
        for code, description in jurisdictions.items():
            writer.writerow(['jur-' + code, code, description])

    # Write serviceProviders file
    print "  * Write file [ServiceProviders]"
    with open(targetDir + 'ServiceProviders.csv', 'wb') as serviceFile:
        writer = csv.writer(serviceFile, delimiter = ',')
        for code, description in serviceProviders.items():
            writer.writerow([code, description])

    # Write entity types file
    print "  * Write file [EntityTypes]"
    with open(targetDir + 'EntityTypes.csv', 'wb') as typeFile:
        writer = csv.writer(typeFile, delimiter = ',')
        for code, description in entityTypes.items():
            writer.writerow([code, description])

    # Write additional relationships
    print "  * Write file [additional_relationships_entity"
    with open(targetDir + 'additional_relationships_entity.csv', 'wb') as addRel:
        writer = csv.writer(addRel, delimiter = ',')
        for _, item in enumerate(additional_relationships):
            writer.writerow(item)

    return {'countries': countries, 'relToCountry': entityToCountry}

######################################################################################################################
#                                                   ADDRESSSES                                                       #
######################################################################################################################
def manageAddresses(sourceDir, targetDir, countries):
    """Import and convert data from Addresses.csv"""

    print "==========> Import and convert data from " + sourceDir + "Addresses.csv to " + targetDir + "Addresses.csv"

    writeHeaders(targetDir, 'Addresses', ['uid:ID', 'description'])

    addressToCountry = {}

    #Manage Officers data
    print "  * Write file"
    with open(sourceDir + 'Addresses.csv', 'rb') as source:
        reader = csv.DictReader(source, delimiter = ',')
        with open(targetDir + 'Addresses.csv', 'wb') as target:
            writer = csv.writer(target, delimiter = ',')
            for row in reader:
                #Manage empty country info
                if row['country_codes'] == '':
                    row['country_codes'] = 'XXX'
                    row['countries'] = 'Not identified'

                #Countries can be an string separated by semi-colon
                countryCodeList = row['country_codes'].split( ';')
                countryNameList = row['countries'].split(';')
                for countryCode, countryName in zip(countryCodeList, countryNameList):
                    countries[countryCode] = countryName
                    addressToCountry[row['node_id']] = countryCode

                writer.writerow([row['node_id'], row['address']])

    return {'countries': countries, 'relToCountry': addressToCountry}

######################################################################################################################
#                                                   INTERMEDIARIES                                                   #
######################################################################################################################
def manageIntermediaries(sourceDir, targetDir, countries):
    """Import and convert data from Intermediaries.csv"""

    print "==========> Import and convert data from " + sourceDir + "Intermediaries.csv to " + targetDir + "Intermediaries.csv"

    writeHeaders(targetDir, 'Intermediaries', ['uid:ID', 'name', 'address', 'status'])

    intermediaryToCountry = {}
    intermediariesId = []

    #Manage Officers data
    print "  * Write file"
    with open(sourceDir + 'Intermediaries.csv', 'rb') as source:
        reader = csv.DictReader(source, delimiter = ',')
        with open(targetDir + 'Intermediaries.csv', 'wb') as target:
            writer = csv.writer(target, delimiter = ',')
            for row in reader:
                #Manage empty country info
                if row['country_codes'] == '':
                    row['country_codes'] = 'XXX'
                    row['countries'] = 'Not identified'

                #Countries can be an string separated by semi-colon
                countryCodeList = row['country_codes'].split( ';')
                countryNameList = row['countries'].split(';')
                for countryCode, countryName in zip(countryCodeList, countryNameList):
                    countries[countryCode] = countryName
                    intermediaryToCountry[row['node_id']] = countryCode

                writer.writerow([row['node_id'], row['name'], row['address'], row['status']])
                intermediariesId.append(row['node_id'])

    return {'countries': countries, 'relToCountry': intermediaryToCountry, 'intermediariesId': intermediariesId}

######################################################################################################################
#                                                   ALL EDGES                                                        #
######################################################################################################################
def manageAllEdges(sourceDir, targetDir):
    """Import and convert data from all_edges.csv"""

    print "==========> Import and convert data from " + sourceDir + "all_edges.csv to " + targetDir + "all_edges.csv"

    writeHeaders(targetDir, 'all_edges', [':START_ID', ':END_ID', ':TYPE'])

    print "  * Write file"
    with open(sourceDir + 'all_edges.csv', 'rb') as source:
        reader = csv.DictReader(source)
        with open(targetDir + 'all_edges.csv', 'wb') as target:
            writer = csv.writer(target, delimiter = ',')
            for row in reader:
                cleanType = re.sub('[^0-9a-zA-Z]+', '_', row['rel_type']).upper()
                writer.writerow([row['node_1'], row['node_2'], cleanType])

######################################################################################################################
#                                                   COUNTRIES                                                        #
######################################################################################################################
def addCountryRelationships(targetDir, relationshipDefinition, itemType):
    """Add Node to Country relationship to additional_relationships.csv"""

    print "==========> Add Country relationships"

    filePrefix = 'additional_relationships_country_' + itemType

    # Create headers file if not exists
    if False == os.path.isfile(targetDir + filePrefix + '_headers.csv'):
        print "  * Create headers"
        with open(targetDir + filePrefix + '_headers.csv', 'wb') as headerFile:
            writer = csv.writer(headerFile, delimiter = ',')
            writer.writerow([':START_ID', ':END_ID', ':TYPE'])

    # Add country relationships
    print "  * Write relationhips"
    with open(targetDir + filePrefix + '.csv', 'wb') as relationhipFile:
        writer = csv.writer(relationhipFile, delimiter = ',')
        for source, target in relationshipDefinition.items():
            writer.writerow([source, target, 'IS_IN_COUNTRY'])

def saveCountries(targetDir, countries):
    """Creates country files"""

    print "==========> Creates country file"

    writeHeaders(targetDir, 'Countries', ['code:ID', 'name'])

    print "  * Wrtie file [Countries.csv]"
    with open(targetDir + 'Countries.csv', 'wb') as file:
        writer = csv.writer(file)
        for code, name in countries.items():
            writer.writerow([code, name])

######################################################################################################################
#                                                   USEFUL                                                           #
######################################################################################################################
def writeHeaders(targetDir, filePrefix, headers):
    print "  * Create headers for [" + filePrefix + "]"
    with open(targetDir + filePrefix + '_headers.csv', 'wb') as headersFile:
        writer = csv.writer(headersFile, delimiter = ',')
        writer.writerow(headers)