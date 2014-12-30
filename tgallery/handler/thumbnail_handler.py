from http.client import NOT_FOUND, BAD_REQUEST
import logging
import os
import re
from tornado import gen

from tornado.web import HTTPError
from tgallery.handler.base_handler import BaseHandler
from tgallery.helper.picture_cache import PictureCache
from tgallery.helper.process_pool import ProcessPool
from tgallery.helper.picture import Picture

LOG = logging.getLogger()

IMAGE_SUFFIX = ('jpeg', 'jpg')
THUMBNAIL_REGEXP = re.compile(r'(.+)/thumbnail/(\d+)x(\d+)$')


class ThumbnailHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        self.x_size = 0
        self.y_size = 0
        super(ThumbnailHandler, self).__init__(*args, **kwargs)

    @gen.coroutine
    def get(self, path):
        LOG.debug('Getting thumbnail for %s', path)
        if os.path.sep != "/":
            path = path.replace("/", os.path.sep)

        filepath, self.x_size, self.y_size = ThumbnailHandler._parse_path(path)
        abs_path = self.get_validated_absolute_path(filepath)

        if not os.path.isfile(abs_path):
            raise HTTPError(NOT_FOUND, 'File {} not found'.format(path))

        self.set_header('Content-Type', 'image/jpeg')

        thumbnail_key = '{}/thumbnail/{}x{}'.format(abs_path, self.x_size, self.y_size)
        thumbnail = PictureCache.instance().lookup(thumbnail_key)
        if not thumbnail:
            LOG.debug('submitting thumbnail generation for {} size {} {}'.format(abs_path, self.x_size, self.y_size))
            thumbnail = yield ProcessPool.instance().submit(_gen_thumbnail_content, abs_path, self.x_size, self.y_size)
            PictureCache.instance().store(thumbnail_key, thumbnail)

        self.write(thumbnail)
        self.finish()

    @staticmethod
    def _parse_path(path):
        thumbnail = THUMBNAIL_REGEXP.search(path)
        if not thumbnail:
            raise HTTPError(BAD_REQUEST, 'Invalid thumbnail request {}'.format(path))
        path, x_str, y_str = thumbnail.groups()
        return path, int(x_str), int(y_str)


def _gen_thumbnail_content(absolute_path, x_size, y_size):
    LOG.debug('start gen')
    picture = Picture(absolute_path)
    picture.resize(x_size, y_size)
    content = picture.get_content()
    LOG.debug('done')
    return content




