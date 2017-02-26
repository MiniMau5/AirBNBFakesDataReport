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
        # send_mail_list('test', 'my-first-email')
        # author = "Kemal Ahmed"
        # filename = "test4938sdsd2"
        # filename = filename.replace(" ", "-")
        # filename = filename.replace("_", "-")
        # author = author.replace(" ", "-")
        # author = author.replace("_", "-")
        # key = author + "_" + filename
        view = "community"
        query = ["triangle",""]
        response = yield derp.db_query("default", "communote", view, tag=query, limit=20, index=0)
        # response = yield derp.db_insert("beer-sample", key, {"title": filename, "authors": [{"name": author}]})

        self.write(str(response))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()


