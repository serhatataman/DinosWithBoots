import json

attributes = {}
file_count = 0

# Read metadata/all-objects.json and find duplicate properties
with open('metadata/all-objects.json') as f:
    d = json.load(f)
    for token in d:
        unique_value = str(token['Accessory']) \
                       + '_' + str(token['Background']) \
                       + '_' + str(token['Eyes']) \
                       + '_' + str(token['Shoes']) \
                       + '_' + str(token['Skeleton']) \
                       + '_' + str(token['Skin']) \
                       + '_' + str(token['Tail']) \
                       + '_' + str(token['Teeth'])

        # if background is not a duplicate, skip it
        if unique_value not in attributes.values():
            attributes[token['tokenId']] = unique_value
        else:
            print('\nDuplicate: ' + str(token['tokenId']) + ' ' + str(unique_value))
