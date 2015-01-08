from pkg_resources import resource_filename
from os import path
import tornado.ioloop
from tornado.web import StaticFileHandler
import logging
from tornado.options import options, define
from tornado.process import cpu_count
from tgallery.handler.metadata_handler import MetadataHandler
from tgallery.handler.thumbnail_handler import ThumbnailHandler
from tgallery.handler.gallery_handler import GalleryHandler
from tgallery.services.picture_cache import PictureCache
from tgallery.services.process_pool import ProcessPool
LOG = logging.getLogger()

STATIC_PATH = path.join(resource_filename('tgallery', '.'), 'static')


define('picture_path', default='~/Pictures', help='Picture path exposed as gallery root.')
define('debug', default='off', help='Set to "on" if debug mode (autoreloading) should be enabled.')


def main():
    options.parse_command_line()
    debug = options.debug == 'on'

    PictureCache.init()
    ProcessPool.init(max_workers=cpu_count())
    application = tornado.web.Application(
        [
            (r'/static/(.+)', StaticFileHandler, {'path': STATIC_PATH}),
            (r'/filepath/()', GalleryHandler, {'path': options.picture_path}),
            (r'/filepath/(.+)/', GalleryHandler, {'path': options.picture_path}),
            (r'/filepath/(.+)/thumbnail/([0-9]+)x([0-9]+)', ThumbnailHandler, {'path': options.picture_path}),
            (r'/filepath/(.+)/metadata', MetadataHandler, {'path': options.picture_path}),
            (r'/filepath/(.+)', StaticFileHandler, {'path': options.picture_path}),
            (r'/(.*)', StaticFileHandler, {'path': STATIC_PATH, 'default_filename': 'index.html'}),
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
