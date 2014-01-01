import os

import tornado.ioloop
import tornado.web
from tornado.options import options, define

from tgallery import module_locator
from tgallery.gallery_handler import GalleryHandler


static_path = os.path.join(module_locator.module_path(), 'static')

define('picture_path', default='~/Pictures', help='Picture path exposed as gallery root.')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, this is tornado gallery.')


def main():
    options.parse_command_line()
    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
        (r'/gallery/(.*)', GalleryHandler, {'path': options.picture_path}),
    ])
    application.listen(1234)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
