from tornado import httpclient
from tornado import escape
import tornado
from tornado import *

import os
from math import ceil
import sys
import re
import csv
# import urllib2
# import urllib

import json

# Constants

# search_location = urllib.pathname2url("Geneva, Switzerland")
search_location = escape.url_escape("Geneva, Switzerland", plus=False)
numGuests = str(4)


# Open csv file for writing
# resultsFile = open('results.txt', 'a+')
f = csv.writer(open('AirbnbData.csv', 'w'))
f.writerow(["number", "id", "bathrooms","bedrooms","beds","instant_bookable","is_new_listing", "person_capacity", "property_type", "reviews_count", "room_type"])


http = httpclient.AsyncHTTPClient()
headers = {'User-Agent': 'Magic Browser'}

loop = tornado.ioloop.IOLoop.current()

@tornado.gen.coroutine
def queue_requests():
    
    # 1) asynchronous calls with callbacks (getting lists of results)
    # TODO: change this to 1000 when you're ready
    results_num = 50
    results = []
    for i in range(int(ceil(results_num/50.0))):
        nxt = tornado.gen.sleep(1)  # 1 request per second
    
        url = gen_url(i, search_location)
        print "search results being fetched"
        res = http.fetch(httpclient.HTTPRequest(url, 'GET', headers), handle_response)
        results.append(res)
        print "fetch sent"
        yield nxt
    yield results
    loop.add_callback(loop.stop)

@tornado.gen.coroutine
def handle_response(response):
    print "response handling commencing..."
    if response.error:
        print "Error:", response.error
    elif response.code == 200:
        # TODO: handle response
        print "response handled"

        results = json.loads(response.body)
        # results = json.load(response.body)

        # find number of results in json file

        # print len(req['search_results'])
        # create counter for tracking in file
        count = 0

        # TODO: separate ids
        ids = results['search_results']
        for key in ids:
            count = count + 1
            try:
                room_id=key["listing"]
                print "fetching room"
                yield fetch_ids(room_id)
            # TODO: is the indent correct here??
            except:
                print "failure to fetch room"
    else:
        print "failure: ", response.code

# 2) asynchronous calls with generators (parsing, getting descriptions from ids)
@tornado.gen.coroutine
def fetch_ids(room_id):
    # create counter for tracking in file
    count = 0
    fetch_results = []
    # construct url
    url = "https://api.airbnb.com/v2/listings/" + room_id + "?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3"
    # url = "" + room_id
    try:
        response =  http.fetch(httpclient.HTTPRequest(url, 'GET', headers), listing_info)
        fetch_results = json.load(response)
        
        # TODO: put results into file
        for key in fetch_results['search_results']:
            count = count + 1
            try:
                #y is the dict code for each listing retrieved
                y = key["listing"]
                # print count, "dictionary"
                # write to each row - important info for each listing - especially id - to be used for further investigation
                # name and city were not used - as they had accents - which caused UnicodeencodeError - ascii codec can't encode...
                f.writerow( [count, y["id"], y["bathrooms"],y["bedrooms"], y["beds"],  y["instant_bookable"], y["is_new_listing"], y["person_capacity"], y["property_type"], y["reviews_count"], y["room_type"]])
        
            except:
                print key, count, "failure writing listing"
    except:
       print count, "failure", url

# TODO: handle response
@tornado.gen.coroutine
def listing_info(response):
    print "listing info handling commencing..."

def gen_url(num, location):
    print num
    # construct URL

    url = "https://api.airbnb.com/v2/search_results?"
    url += "client_id=3092nxybyb0otqw18e8nh5nty"
    # url += "&locale=en-US&currency=USD"
    url += "&_format=for_search_results_with_minimal_pricing"
    url += "&_limit=50"
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
    print "url generated"
    return url

loop.add_callback(queue_requests)
loop.start()
print "done"
