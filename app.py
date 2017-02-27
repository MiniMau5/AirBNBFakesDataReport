from tornado import gen
from tornado import httpclient
import sys
import re

try:
    import simplejson as json
except ImportError:
    import json

http = httpclient.AsyncHTTPClient()
headers = {'User-Agent': 'Magic Browser'}

@gen.coroutine
def try_bb():
    response = "Hello, world"
    
    # TODO: change this to 1000 when you're ready
    results_num = 50

    for i in range(results_num/50):
        yield parse_search(i)


# 1) asynchronous calls with callbacks (getting lists of results)
@gen.coroutine
def parse_search(i):
    url = gen_url(i)
    try:
        # TODO: handle response
        http.fetch(httpclient.HTTPRequest(url, 'GET', headers))
        print url
        
        # TODO: separate ids
        ids = []
        for room_id in ids:
            yield fetch_ids(room_id)
    except:
        print i, "failure"


# 2) asynchronous calls with generators (parsing, getting descriptions from ids)
@gen.coroutine
def fetch_ids(room_id):
    # TODO: construct url
    url = "" + room_id
    try:
        # TODO: handle response
        http.fetch(httpclient.HTTPRequest(url, 'GET', headers))
        # TODO: put results into file
    except:
        print i, "failure"
    
    

def gen_url(num):
    print num
    # TODO: construct URL
    url = "https://api.airbnb.com/v2/search_results?client_id=3092nxybyb0otqw18e8nh5nty"
    return url


try_bb()

