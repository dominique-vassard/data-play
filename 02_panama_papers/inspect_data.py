import csv, sys, re
from collections import Counter, defaultdict

# Inspect data and test id creation
#
# Takes one argument:
#  the directoyr where dat are stored

dataDir = sys.argv[1]

print '=========> Different relationships types <========='
relTypes = []
with open(dataDir + 'all_edges.csv', 'rb') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # relTypes.append(re.sub('[^0-9a-zA-Z]+', '_', row['rel_type']).upper())
        relTypes.append(row['rel_type'])
print Counter(relTypes)

print '=========> Different countries <========='
countries = defaultdict(list)
with open(dataDir + '/Officers.csv', 'rb') as officersFile:
    reader = csv.DictReader(officersFile, delimiter = ',')
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

print Counter(countries);

print '=========> Different jurisdiction <========='
jurisdictions = defaultdict(list)
with open(dataDir + '/Entities.csv', 'rb') as entitiesFile:
    reader = csv.DictReader(entitiesFile, delimiter = ',')
    for row in reader:
        #Manage empty country info
        if row['jurisdiction'] == '':
            row['jurisdiction'] = 'XXX'
            row['jurisdiction_description'] = 'Undetermined'

        jurisdictions[row['jurisdiction']] = row['jurisdiction_description']
print Counter(jurisdictions)

print '=========> Different service provider <========='
serviceProviders = defaultdict(list)
with open(dataDir + '/Entities.csv', 'rb') as entitiesFile:
    reader = csv.DictReader(entitiesFile, delimiter = ',')
    for row in reader:
        #Manage empty service provider info
        if row['service_provider'] == '':
            spId = 'XXX'
            row['service_provider'] = 'Undetermined'
        else:
            spId = ''
            details = row['service_provider'].split()
            for _, detail in enumerate(details):
                spId += detail[:1]

        serviceProviders[spId] = row['service_provider']
print Counter(serviceProviders)

print '=========> Different entityTypes <========='
entityTypes = defaultdict(list)
with open(dataDir + '/Entities.csv', 'rb') as entitiesFile:
    reader = csv.DictReader(entitiesFile, delimiter = ',')
    for row in reader:
        #Manage empty service provider info
        if row['company_type'] == '':
            typeId = 'XXX'
            row['company_type'] = 'Undetermined'
        else:
            typeId = ''
            details = row['company_type'].split()
            for _, detail in enumerate(details):
                typeId += detail[:1] + str(len(detail))

        entityTypes[typeId] = row['company_type']
print Counter(entityTypes)