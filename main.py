import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from urls import urls
from tornado.options import define, options


define("port", default=8124, type=int)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(urls,
                                  debug=True
                                  )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
