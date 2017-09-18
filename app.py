# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from settings import settings
import urls


class Application(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        tornado.web.Application.__init__(self, urls.url_handlers, **settings)


def main():
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
