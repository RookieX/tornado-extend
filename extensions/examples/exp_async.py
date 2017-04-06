#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time

import tornado.web
import tornado.httpserver
import tornado.ioloop

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from extensions import async


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/sleep', SleepHandler),
            (r'/justnow', JustNowHandler)
        ]

        super(Application, self).__init__(handlers=handlers)


class SleepHandler(tornado.web.RequestHandler):
    @async.AsyncHandlerExecutor()
    def get(self):
        result = yield self._async_run(self.sleep)
        self.write(result)

    def sleep(self):
        time.sleep(5)
        return 'sleep over'


class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('just now')


if __name__ == '__main__':
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8888, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
