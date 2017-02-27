from tornado import gen
import tornado.ioloop
import tornado.web
import sys
import re


import settings
import src.scripts.database as derp

try:
    import simplejson as json
except ImportError:
    import json

class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        response = "Hello, world"

        # construct url at some point
        url = "https://api.airbnb.com/v2/search_results?"
        http = tornado.httpclient.AsyncHTTPClient()
        headers = {'User-Agent': 'Magic Browser'}

        # 1) asynchronous calls with callbacks (getting lists of results)
        # tornado.httpclient.HTTPRequest(url, 'GET', headers)
        http.fetch(tornado.httpclient.HTTPRequest(url, 'GET', headers))

        # 2) asynchronous calls with generators (parsing, getting descriptions from ids)
        resultsNum = 1000

        for i in range(resultsNum/50):
            response = yield parseSearch()

        self.write(str(response))

@gen.coroutine
def parseSearch():
    gen.Return("hi")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()


