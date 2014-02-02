import os

import tornado.ioloop
import tornado.web
from tornado.options import options, define

from tgallery import module_locator
from tgallery.handler.gallery_handler import GalleryHandler


STATIC_PATH = os.path.join(module_locator.module_path(), 'static')

define('picture_path', default='~/Pictures', help='Picture path exposed as gallery root.')
define('debug', default='off', help='Set to "on" if debug mode (autoreloading) should be enabled.')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, this is tornado gallery.')


def main():
    options.parse_command_line()
    debug = options.debug == 'on'
    application = tornado.web.Application(
        [
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH}),
            (r'/filepath/(.*)', GalleryHandler, {'path': options.picture_path}),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH, 'default_filename': 'index.html'}),
        ],
        gzip=True,
        debug=debug
    )
    application.listen(1234)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()