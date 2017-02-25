import json

import csv

#choose file for reading / this file has been modified - metadata has been removed to simplify 
json_file='resultsJ.json'
#read json file
readFile = open(json_file, 'r')
x = json.loads(readFile.read())

hosting_data = x['search_results']

# open a file for writing
f = csv.writer(open('AirbnbData.csv', 'w'))

# write the headers to csv file

f.writerow(["number", "id", "bathrooms","bedrooms","beds","instant_bookable","is_new_listing", "person_capacity", "property_type", "reviews_count", "room_type"])

# find number of results in json file
print len(x['search_results'])
#create counter for tracking in file
count=0

for key in x['search_results']:
	count = count +1

	#y is the dict code for each listing retrieved
	y=key["listing"]
	# write to each row - important info for each listing - especially id - to be used for further investigation
	# name and city were not used - as they had accents - which caused UnicodeencodeError - ascii codec can't encode...
	f.writerow( [count, y["id"], y["bathrooms"],y["bedrooms"], y["beds"],  y["instant_bookable"], y["is_new_listing"], y["person_capacity"], y["property_type"], y["reviews_count"], y["room_type"]])

readFile.close()

# closing of csv file ?? f.close()  did not work