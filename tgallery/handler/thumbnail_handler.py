from http.client import NOT_FOUND, BAD_REQUEST
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
        abs_path = self.get_validated_absolute_path(file_path)
        self.x_size, self.y_size = int(x_size), int(y_size)

        if not os.path.isfile(abs_path):
            raise HTTPError(NOT_FOUND, 'File {0} not found'.format(file_path))

        self.set_header('Content-Type', 'image/jpeg')

        thumbnail_key = '{0}/thumbnail/{1}x{2}'.format(abs_path, self.x_size, self.y_size)
        thumbnail = PictureCache.instance().lookup(thumbnail_key)
        if not thumbnail:
            LOG.debug('submitting thumbnail generation for {0} size {1} {2}'.format(abs_path, self.x_size, self.y_size))
            thumbnail = yield ProcessPool.instance().submit(_gen_thumbnail_content, abs_path, self.x_size, self.y_size)
            PictureCache.instance().store(thumbnail_key, thumbnail)

        self.write(thumbnail)
        self.finish()


def _gen_thumbnail_content(absolute_path, x_size, y_size):
    picture = Picture(absolute_path)
    picture.resize(x_size, y_size)
    return picture.get_content()





