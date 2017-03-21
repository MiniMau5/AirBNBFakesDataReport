from tornado import httpclient
from tornado import escape
import tornado
from tornado import *

import os
from math import ceil
import sys
import re
import csv
import datetime

import logging
# from pprint import pformat
# from pprint_data import data

logging.basicConfig(filename='logs/log_' + datetime.datetime.utcnow().isoformat() + '.txt', level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s',
                    )

logging.debug('Logging pformatted data')
# logging.debug(pformat(data))

import json

import scanner

# Constants

# search_location = urllib.pathname2url("Geneva, Switzerland")
search_location = escape.url_escape("Geneva, Switzerland", plus=False)
numGuests = str(4)


# Open csv file for writing
# resultsFile = open('results.txt', 'a+')
f = csv.writer(open('AirbnbData.csv', 'w'))
f.writerow(["number", "id","Sketchy?" "bathrooms","bedrooms","beds","instant_bookable","description", "person_capacity", "property_type", "reviews_count", "room_type"])
overall_count=0

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
        logging.debug("search results being fetched")
        res = http.fetch(httpclient.HTTPRequest(url, 'GET', headers), handle_response)
        results.append(res)
        logging.debug("fetch sent")
        yield nxt
    yield results
    # loop.add_callback(loop.stop)

@tornado.gen.coroutine
def handle_response(response):
    logging.debug("response handling commencing...")
    if response.error:
        logging.debug("Error:")
        # logging.debug(response.error)
    elif response.code == 200:
        # TODO: handle response
        logging.debug("response handled")

        results = json.loads(response.body)
        # results = json.load(response.body)

        # find number of results in json file

        logging.debug(len(results['search_results']))
        # create counter for tracking in file
        count = 0

        # TODO: separate ids
        ids = results['search_results']
        for key in ids:
            # count = count + 1
            try:
                nxt = tornado.gen.sleep(1)  # 1 request per second
                room_id = key["listing"]["id"]
                logging.debug("**** FETCHING ROOM  #")
                logging.debug(room_id)
                yield fetch_ids(room_id)
                yield nxt
            # TODO: is the indent correct here??
            except:
                logging.debug("failure to fetch room")
    else:
        logging.debug("failure: ")
        logging.debug(response.code)

# 2) asynchronous calls with generators (parsing, getting descriptions from ids)
@tornado.gen.coroutine
def fetch_ids(room_id):
    # create counter for tracking in file
    # count = 0
    fetch_results = []
    # construct url
    url = "https://api.airbnb.com/v2/listings/" + str(room_id) + "?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3"
    # url = "" + room_id
    logging.debug(url)
    try:
        # nxt = tornado.gen.sleep(1)  # 1 request per second
        logging.debug("listing info handling commencing...in fetch ids")
        response = http.fetch(httpclient.HTTPRequest(url, 'GET', headers), listing_info)
        fetch_results.append(response)
        logging.debug("results have been fetched")
        # yield nxt
    except:
       logging.debug("failure ")
       logging.debug(room_id)
    logging.debug("results have been fetched here")
    yield fetch_results
    
# TODO: handle response
@tornado.gen.coroutine
def listing_info(response):
    global overall_count
    logging.debug("response handling commencing... in listing info")
    if response.error:
        logging.debug("Error:")
        logging.debug(response.error)
    elif response.code == 200:
        # TODO: handle response
        logging.debug("response handled -in listing info")

        overall_count = overall_count +1
        logging.debug("listing info")
        try:
            fetch_results = json.loads(response.body)
            y = fetch_results['listing']
            # TODO: put results into file
            logging.debug('count:')
            logging.debug(overall_count)
            # logging.debug(y)
            # print y["id"], y["bathrooms"],y["bedrooms"], y["beds"],  y["instant_bookable"], y["description"], y["person_capacity"], y["property_type"], y["reviews_count"], y["room_type"]
            sketchy = scanner.isSketchy(y["description"])
            logging.debug(sketchy)
            # TODO: csv headers
            f.writerow( [overall_count, y["id"], sketchy, y["bathrooms"],y["bedrooms"], y["beds"],  y["instant_bookable"], y["description"], y["person_capacity"], y["property_type"], y["reviews_count"], y["room_type"]])
        except:
            logging.debug("Error: Listing info not found")

def gen_url(num, location):
    logging.debug("****   ")
    logging.debug(num)
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
    # logging.debug("url generated")
    return url

loop.add_callback(queue_requests)
loop.start()
print "done"
