# -*- coding: utf-8 -*-
import tornado


class SignalHandler(tornado.web.RequestHandler):

    def get(self):
        print('get')
