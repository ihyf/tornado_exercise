#!/usr/bin/env python
#-*- coding: utf-8 -*

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import define, options
from pycket.session import SessionMixin

define('port', default=8888, help='fuck', type=int)
define('debug', default=False, help='fuck', type=bool)


class HomeHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


class LoginHandler(tornado.web.RequestHandler, SessionMixin):

    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        print self.get_argument('user', None)
        self.set_secure_cookie('user', self.get_argument('user', None))
        self.session.set('user_session', self.get_argument('user', None))
        self.write('Successfully set cookie!')


class OtherHtmlHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user = self.get_secure_cookie('user')
        return user

    @tornado.web.authenticated
    def get(self, page):
        #import pdb
        # pdb.set_trace()
        # if not self.current_user:
        #     self.redirect("/login.html")
        #     return
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

    def __init__(self, debug=False):
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
            'xsrf_cookies': True,
            'debug': debug,
            'pycket': {
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    'db_sessions': 10,
                    'db_notifications': 11,
                    'max_connections': 2**31,
                }
            }
        }
        super(CustomApplication, self).__init__(handles, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    # 实例化一个httpserver对象
    http_server = tornado.httpserver.HTTPServer(CustomApplication(debug=options.debug))
    # 监听8888 套接字端口
    http_server.listen(options.port)
    # 启动事件循环
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
