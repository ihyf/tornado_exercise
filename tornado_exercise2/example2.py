#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web


class HomeHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


class LoginHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        self.set_secure_cookie('user', self.get_argument('user', None))
        self.write('Successfully set cookie!')


class OtherHtmlHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user = self.get_secure_cookie('user')
        return user

    def get(self, page):
        #import pdb
        # pdb.set_trace()
        if not self.current_user:
            self.redirect("/login.html")
            return
        pagename = page + '.html'
        path = os.path.join(self.settings['static_path'], pagename)
        print path
        self.render(pagename)


class OtherHandler(tornado.web.RequestHandler):

    def get(self, page, extension):
        pagename = page + '.' + extension
        path = os.path.join(self.settings['static_path'], pagename)
        print path
        if extension != 'html':
            with open(path) as f:
                self.write(f.read())


class CustomApplication(tornado.web.Application):

    def __init__(self):
        handles = [
            (r'/$', HomeHandler),
            (r'/login.html', LoginHandler),
            (r'/(.+?)\.html', OtherHtmlHandler),
            (r'/(.+?)\.(.+)', OtherHandler),
        ]
        settings = {
            'template_path': os.path.join(
                os.path.dirname(__file__),
                'startbootstrap-clean-blog'),
            'static_path': os.path.join(
                os.path.dirname(__file__),
                'startbootstrap-clean-blog'),
            'login_url': '/login.html',
            'cookie_secret': "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o",
            'xsrf_cookies': True}
        super(CustomApplication, self).__init__(handles, **settings)


if __name__ == '__main__':
    # 实例化一个httpserver对象
    http_server = tornado.httpserver.HTTPServer(CustomApplication())
    # 监听8888 套接字端口
    http_server.listen(8888)
    # 启动事件循环
    tornado.ioloop.IOLoop.instance().start()
