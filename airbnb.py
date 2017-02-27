import urllib2
import urllib
import json
import sys

import csv

# from urllib import urlencode
# import urllib.urlencode


# connect using the unofficial airbnb api: http://airbnbapi.org/

searchLocation = urllib.pathname2url("Geneva, Switzerland")
numGuests = str(4)
resultsFile = open('results.txt', 'a+')
results = []


# return value of url with beginning search range
def url_range(start):
    url = "https://api.airbnb.com/v2/search_results?"
    url += "client_id=3092nxybyb0otqw18e8nh5nty"
    # url += "&locale=en-US&currency=USD"
    url += "&_format=for_search_results_with_minimal_pricing"
    url += "&_limit=50"
    url += "&_offset=" + str(50 * start)
    url += "&fetch_facets=false"
    # url += "&guests=" + numGuests
    url += "&ib=false&ib_add_photo_flow=true"
    url += "&location=" + searchLocation
    # url += "&location=Lake%20Tahoe%2C%20CA%2C%20US"
    url += "&min_bathrooms=1&min_bedrooms=0&min_beds=1"
    url += "&min_num_pic_urls=10"
    url += "&price_max=210&price_min=40"
    # url += "&sort=1"
    # url += "&user_lat=37.3398634&user_lng=-122.0455164"
    return url

# fetch function
# http://airbnbapi.org/#view-listing-info

for i in range(1):
    url = url_range(i)

    req = urllib2.Request(url, headers={'User-Agent': 'Magic Browser'})
    print i
    print url
    try:
        f = urllib2.urlopen(req)
        results = json.load(f)
        # results.append(f.read())
        # results2=(f.read())
        # resultsFile.write("open")
        # resultsFile.write(str(results.pop()))
        # resultsFile.write(str(f.read()))
    except:
        results.append("failure")
        resultsFile.write("failure")
        print "Unexpected error:", sys.exc_info()[0]
    print "DONE"

    print results
    hosting_data = results['search_results']

    # open a file for writing
    f = csv.writer(open('AirbnbData.csv', 'w'))

    # write the headers to csv file

    f.writerow(["number", "id", "bathrooms","bedrooms","beds","instant_bookable","is_new_listing", "person_capacity", "property_type", "reviews_count", "room_type"])

    # find number of results in json file
    print len(results['search_results'])
    #create counter for tracking in file
    count=0

    for key in results['search_results']:
        count = count +1

        #y is the dict code for each listing retrieved
        y=key["listing"]
        # write to each row - important info for each listing - especially id - to be used for further investigation
        # name and city were not used - as they had accents - which caused UnicodeencodeError - ascii codec can't encode...
        f.writerow( [count, y["id"], y["bathrooms"],y["bedrooms"], y["beds"],  y["instant_bookable"], y["is_new_listing"], y["person_capacity"], y["property_type"], y["reviews_count"], y["room_type"]])
    print ("finished")
    # readFile.close()
    # resultsFile.write("DONE")
    resultsFile.close()

