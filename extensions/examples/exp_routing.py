#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import tornado.web
import tornado.httpserver
import tornado.ioloop

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from extensions.routing import route


# 用法1
# class Application(tornado.web.Application):
#     def __init__(self):
#         super(Application, self).__init__(handlers=route.routes())

class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__()


@route(r'/home')
class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Home')


@route(r'/about')
class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('About')


if __name__ == '__main__':
    app = Application()

    # 用法2
    route.register_routes(app)

    server = tornado.httpserver.HTTPServer(app)
    server.listen(8888, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
