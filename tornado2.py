from tornado.httpclient import AsyncHTTPClient
import tornado

URLS = ['https://api.airbnb.com/v2/listings/5116458?client_id=3092nxybyb0otqw18e8nh5nty&locale=en-US&currency=USD&_format=v1_legacy_for_p3&_source=mobile_p3&number_of_guests=1']
http_client = AsyncHTTPClient()
headers = {'User-Agent': 'Magic Browser'}

loop = tornado.ioloop.IOLoop.current()


def handle_request(response):
    if response.code == 200:
        with open('json_output.txt', 'a') as outfile:
            outfile.write(response.body)


@tornado.gen.coroutine
def queue_requests():
    results = []
    for url in URLS:
        nxt = tornado.gen.sleep(1)  # 1 request per second
        res = http_client.fetch(tornado.httpclient.HTTPRequest(url, 'GET', headers), handle_request)
        results.append(res)
        yield nxt
    yield results  # wait for all requests to finish
    loop.add_callback(loop.stop)
loop.add_callback(queue_requests)
loop.start()
print "done"
