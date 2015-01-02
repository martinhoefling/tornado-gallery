from http.client import NOT_FOUND
import logging
import os

from tornado import gen
from tornado.web import HTTPError

from tgallery.handler.base_handler import BaseHandler
from tgallery.services.picture_cache import PictureCache
from tgallery.services.process_pool import ProcessPool
from tgallery.util.picture import Picture


LOG = logging.getLogger()


class ThumbnailHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        self.x_size = 0
        self.y_size = 0
        super(ThumbnailHandler, self).__init__(*args, **kwargs)

    @gen.coroutine
    def get(self, file_path, x_size, y_size):
        LOG.debug('Getting thumbnail for %s', file_path)
        if os.path.sep != "/":
            path = file_path.replace("/", os.path.sep)

        self.x_size, self.y_size = int(x_size), int(y_size)
        abs_path = self.get_validated_absolute_path(file_path)

        if not os.path.isfile(abs_path):
            raise HTTPError(NOT_FOUND, 'File {} not found'.format(file_path))

        self.set_header('Content-Type', 'image/jpeg')

        thumbnail_key = '{}/thumbnail/{}x{}'.format(abs_path, self.x_size, self.y_size)
        thumbnail = PictureCache.instance().lookup(thumbnail_key)
        if not thumbnail:
            LOG.debug('submitting thumbnail generation for {} size {} {}'.format(abs_path, self.x_size, self.y_size))
            thumbnail = yield ProcessPool.instance().submit(_gen_thumbnail_content, abs_path, self.x_size, self.y_size)
            PictureCache.instance().store(thumbnail_key, thumbnail)

        self.write(thumbnail)
        self.finish()


def _gen_thumbnail_content(absolute_path, x_size, y_size):
    LOG.debug('start gen')
    picture = Picture(absolute_path)
    picture.resize(x_size, y_size)
    content = picture.get_content()
    LOG.debug('done')
    return content




