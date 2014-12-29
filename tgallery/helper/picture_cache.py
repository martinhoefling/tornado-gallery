from collections import OrderedDict
import logging
import time

LOG = logging.getLogger()


class PictureCache(object):
    _instance = None

    def __init__(self):
        self.cached_pictures = OrderedDict()

    @classmethod
    def init(cls):
        LOG.info('Picture cache initialized')
        cls._instance = cls()

    @classmethod
    def instance(cls):
        assert cls._instance, 'Picture cache not initialized yet'
        return cls._instance

    def lookup(self, imagepath):
        image = self.cached_pictures.get(imagepath, None)
        if image:
            LOG.debug('Image %s in cache', imagepath)
            image['timestamp'] = time.time()
            return image['data']
        else:
            LOG.debug('Image %s in not cache', imagepath)
            return None

    def store(self, imagepath, data):
        self.cached_pictures[imagepath] = {
            'data': data,
            'timestamp': time.time()
        }

