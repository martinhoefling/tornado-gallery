from collections import OrderedDict
import logging
import time

from tgallery.services.base_service import BaseService


LOG = logging.getLogger()


class PictureCache(BaseService):
    _instance = None

    def __init__(self):
        self._cached_pictures = OrderedDict()

    def lookup(self, imagepath):
        image = self._cached_pictures.get(imagepath)
        if image:
            LOG.debug('Image %s in cache', imagepath)
            image['timestamp'] = time.time()
            return image['data']
        else:
            LOG.debug('Image %s in not cache', imagepath)
            return None

    def store(self, imagepath, data):
        self._cached_pictures[imagepath] = {
            'data': data,
            'timestamp': time.time()
        }

