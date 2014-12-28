from pkg_resources import resource_filename
from os import path
import tornado.ioloop
import tornado.web
import logging
from tornado.options import options, define
from tgallery.handler.gallery_handler import GalleryHandler

LOG = logging.getLogger()

STATIC_PATH = path.join(resource_filename('tgallery', '.'), 'static')


define('picture_path', default='~/Pictures', help='Picture path exposed as gallery root.')
define('debug', default='off', help='Set to "on" if debug mode (autoreloading) should be enabled.')


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
    LOG.info('Listening...')
    LOG.info('Asset path is %s', STATIC_PATH)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    LOG = logging.getLogger('tgallery')
    main()
