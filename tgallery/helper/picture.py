import io

from PIL import Image
from libxmp import XMPFiles, XMPError
from libxmp import consts as xmpconsts

import logging
import time
from helper.picture_cache import PictureCache

LOG = logging.getLogger()


def timing(msg, starttime):
    LOG.debug('%s %f ms', msg, (time.time()-starttime) * 1000)


class Picture(object):
    def __init__(self, filename):
        self.filename = filename
        self.metadata = None
        self.image = None

    def _read_metadata(self):
        try:
            startt=time.time()
            self.metadata = XMPFiles(file_path=self.filename).get_xmp()
            timing('Metadata read in', startt)

        except XMPError:
            LOG.debug('Error reading xmp metadata for %s', self.filename)

    def get_metadata(self):
        if not self.metadata:
            self._read_metadata()
        try:
            return {'rating': self.metadata.get_property(xmpconsts.XMP_NS_XMP, 'xmp:Rating')}
        except XMPError:
            return 'Metadata could not be read for {}'.format(self.filename)

    def _read_image(self):
        image = PictureCache.instance().lookup(self.filename)
        if not image:
            image = self._load_image()
            PictureCache.instance().store(self.filename, image)
        self.image = image

    def _load_image(self):
        startt=time.time()
        try:
            image = Image.open(self.filename)
        except OSError:
            image = Image.new('RGB', (800, 800), 'white')
        image.load()
        timing('Image read in', startt)
        return image

    def resize(self, x_size, y_size):
        lookup_key = self.filename + '/thumbnail/{}x{}'.format(x_size, y_size)
        image = PictureCache.instance().lookup(lookup_key)
        if not image:
            image = self._do_resize(x_size, y_size)
            PictureCache.instance().store(lookup_key, image)
        self.image = image

    def _do_resize(self, x_size, y_size):
        if not self.image:
            self._read_image()

        startt = time.time()

        aspect_ratio = self.image.size[0] / self.image.size[1]

        x_target, y_target = self.image.size
        if x_size < x_target:
            x_target = x_size
            y_target = int(x_target / aspect_ratio)
        if y_size < y_target:
            y_target = y_size
            x_target = int(y_target * aspect_ratio)

        if x_target == 0 or y_target == 0:
            x_target = 1
            y_target = 1

        image = self.image.resize((x_target, y_target), Image.ANTIALIAS)
        timing('Image resized in', startt)
        return image

    def get_content(self):
        if not self.image:
            self._read_image()
        buf = io.BytesIO()
        self.image.save(buf, format="JPEG")
        content = buf.getvalue()
        buf.close()
        return content
