#! /usr/bin/env python
# -*- coding: utf-8 -*-

u"""
扩展 `tornado` 的异步机制，避免某个 `Handler` 执行缓慢时阻塞主线程。
用法：
class SleepHandler(tornado.web.RequestHandler):
    @AsyncHandlerExecutor()
    def get(self):
        result = yield self._async_run(self.sleep)
        self.write(result)

    def sleep(self):
        time.sleep(5)
        return 'sleep over'
"""

import functools
from concurrent.futures import ThreadPoolExecutor

import tornado.concurrent


class AsyncHandlerExecutor(object):
    u"""
    给Handler提供异步机制的装饰器，内部维护一个executor对象供tornado.concurrent.run_on_executor使用
    """

    def __init__(self, max_workers=1):
        u"""
        构建异步执行所需的线程池
        """
        self.executor = ThreadPoolExecutor(max_workers)

    def __call__(self, func):
        u"""
        装饰Handler方法，给Handler注入异步执行所需的异步函数
        """

        @functools.wraps(func)
        def _wrapper(handler, *args, **kwargs):
            handler._async_run = self._async_run  # 异步钩子

            # 给Handler添加异步所需的装饰器，方便编程
            @tornado.web.asynchronous
            @tornado.gen.coroutine
            def _async(handler):
                return func(handler, *args, **kwargs)

            return _async(handler)

        return _wrapper

    @tornado.concurrent.run_on_executor
    def _async_run(self, func, *args, **kwargs):
        u"""
        异步函数，其实只是提供了 run_on_executor 的统一装饰
        """
        return func(*args, **kwargs)
