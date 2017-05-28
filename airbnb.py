import urllib
import sys
import requests
from math import ceil
import csv
import datetime
import logging

import scanner

# inputs

search_location = urllib.pathname2url("Geneva, Switzerland")
num_guests = str(4)
results_num = 1000

# constants

results_file = open('results.txt', 'a+')
headers = {'User-Agent': 'Magic Browser'}
    
# open a file for writing
f = csv.writer(open('AirbnbData.csv', 'w'))
    
# write the headers to csv file

f.writerow(
    ["number", "id", "bathrooms", "bedrooms", "beds", "instant_bookable", "is_new_listing", "person_capacity",
     "property_type", "reviews_count", "room_type"])

results = []
overall_count = 0

logging.basicConfig(filename='logs/log_' + datetime.datetime.utcnow().isoformat() + '.txt', level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s',
                    )

logging.debug('Logging pre-formatted data')


# connect using the unofficial airbnb api: http://airbnbapi.org/
# return value of url with beginning search range

def gen_url(num, location):
    logging.debug("****   ")
    logging.debug(num)
    # construct URL
    
    url = "https://api.airbnb.com/v2/search_results?"
    url += "client_id=3092nxybyb0otqw18e8nh5nty"
    # url += "&locale=en-US&currency=USD"
    url += "&_format=for_search_results_with_minimal_pricing"
    url += "&_limit=50" # + str(results_num)
    url += "&_offset=" + str(50 * num)
    url += "&fetch_facets=false"
    # url += "&guests=" + numGuests
    url += "&ib=false&ib_add_photo_flow=true"
    url += "&location=" + location
    # url += "&location=Lake%20Tahoe%2C%20CA%2C%20US"
    
    url += "&min_bathrooms=1&min_bedrooms=0&min_beds=1"
    url += "&min_num_pic_urls=10"
    url += "&price_max=210&price_min=40"
    # url += "&sort=1"
    # url += "&user_lat=37.3398634&user_lng=-122.0455164"
    logging.debug(url)
    return url


def fetch_url(url):
    logging.debug(url)
    try:
        logging.debug("fetching url")
        
        response = requests.get(url, headers=headers)
        logging.debug("results have been fetched")
        
        if response.raise_for_status():
            logging.debug("Error:")
            logging.debug(response.raise_for_status())
        elif response.status_code == 200:
            # TODO: handle response
            logging.debug("response handled -in listing info")
            logging.debug("listing info")
            
            try:
                # fetch_results = json.loads(response.body)
                fetch_results = response.json()
                return fetch_results
            except:
                logging.debug(sys.exc_info()[0])
                logging.debug("^Error: Listing info not found")
        else:
            logging.debug("failure: ")
            logging.debug(response.status_code)
    
    except:
        logging.debug(sys.exc_info()[0])
        logging.debug("failure ")
        logging.debug(room_id)
    return "failure"


def fetch_ids(room_id):
    # construct url
    
    url = "https://api.airbnb.com/v2/listings/" + str(
        room_id) + "?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3"
    # url = "" + room_id
    logging.debug(url)
    
    logging.debug("listing info handling commencing...in fetch ids")
    
    response = fetch_url(url)
    
    # listing_info(response)
    
    logging.debug("results have been fetched")
    
    logging.debug("results have been fetched here")
    return response


# fetch function
# http://airbnbapi.org/#view-listing-info

for i in range(int(ceil(results_num / 50.0))):
    
    # fetching search results
    
    url = gen_url(i, search_location)
    logging.debug("search results being fetched")
    
    search_results = fetch_url(url)
    
    # find number of results in json file
    logging.debug(len(search_results['search_results']))
    
    print len(search_results['search_results'])
    
    # create counter for tracking in file
    
    count = 0
    
    # fetch page data
    
    logging.debug("Fetching page data")
    
    ids = search_results['search_results']
    for key in ids:
        count += 1
        try:
            logging.debug("**** FETCHING ROOM  #")
            room_id = key["listing"]["id"]
        
        except:
            logging.debug(sys.exc_info()[0])
            logging.debug("failure: json not formed properly; no room found")
            break
        
        try:
            logging.debug(room_id)
            room_result = fetch_ids(room_id)
            
        except:
            logging.debug(sys.exc_info()[0])
            logging.debug("failed to fetch id")
            logging.debug(room_id)
            break
        
        results.append(room_result)

        # TODO: put results into file

        logging.debug('count:')
        logging.debug(overall_count)
        y = room_result["listing"]
        sketchy = scanner.isSketchy(y["description"])
        # TODO: csv headers
        f.writerow(
            [overall_count, y["id"], sketchy, y["bathrooms"], y["bedrooms"], y["beds"], y["instant_bookable"],
             y["description"].encode('utf-8'), y["person_capacity"], y["property_type"], y["reviews_count"],
             y["room_type"]])
    
    logging.debug("Finished fetching page data")
        
print "finished"

# results_file.write("DONE")
results_file.close()

