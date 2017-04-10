#! /usr/bin/env python
# -*- coding: utf-8 -*-
u"""
提供路由功能，运行时自动生成路由表
用法：
@route(r'/home')
class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Home')


@route(r'/about')
class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('About')

路由表生成方法1:
class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers=route.routes())

路由表生成方法2:
class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__()

app = Application()
route.register_routes(app)
"""

from itertools import chain

from tornado.web import URLSpec, Application


class _Route(object):
    u"""
    实现路由注册的装饰器
    """
    _route_table = {}

    def __init__(self, pattern, host='.*$', kwargs=None, name=None):
        self.pattern = pattern
        self.host = host
        self.kwargs = kwargs
        self.name = name

    def __call__(self, handler_cls):
        url = URLSpec(self.pattern, handler_cls, self.kwargs, self.name)
        self._add_route(url)
        return handler_cls

    def _add_route(self, url):
        self.__class__._route_table.setdefault(self.host, [])
        self.__class__._route_table[self.host].append(url)

    @classmethod
    def routes(cls):
        u"""
        获取所有路由条目
        """
        return chain(*cls._route_table.values())

    @classmethod
    def register_routes(cls, app):
        u"""
        将路由条目注册到 `Application` 中
        :type app: Application
        """
        [app.add_handlers(pattern, handler) for pattern, handler in cls._route_table.items()]


route = _Route
