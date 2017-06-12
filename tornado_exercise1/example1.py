#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web


class HomeHandler(tornado.web.RequestHandler):

    def test_string(self, message):
        return '<a href>%s</a>' % message

    def get(self, *args, **kwargs):
        self.ui['test_function'] = self.test_string
        self.render(
            'login.html',
            error="",
            message="<h1>test</h1>",
            list=[
                "a",
                'b',
                'c'])


class OtherHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        return 1


class FormHandler(tornado.web.RequestHandler):

    def post(self):
        raise tornado.web.HTTPError(
            status_code=416,
            log_message='testing',
            reason='Form submit is not supported yet!')


class CustomApplication(tornado.web.Application):

    def __init__(self):
        handles = [
            (r'/', HomeHandler),
            (r'/login', HomeHandler),
            (r'/auth/login', FormHandler),
            (r'/.*', OtherHandler),
        ]
        settings = {
            'template_path': os.path.join(
                os.path.dirname(__file__),
                'templates'),
            'static_path': os.path.join(
                os.path.dirname(__file__),
                'static'),
            'blog_title': 'simple blog'}
        super(CustomApplication, self).__init__(handles, **settings)


if __name__ == '__main__':
    # 实例化一个httpserver对象
    http_server = tornado.httpserver.HTTPServer(CustomApplication())
    # 监听8888 套接字端口
    http_server.listen(8888)
    # 启动事件循环
    tornado.ioloop.IOLoop.instance().start()
