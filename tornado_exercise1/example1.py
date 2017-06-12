#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json


class HomeHandler(tornado.web.RequestHandler):


    def get(self, *args, **kwargs):
        self.write("111")


class OtherHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        data = {'name': "hyf"}
        return json.dump(data)


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
