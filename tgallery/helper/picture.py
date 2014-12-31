import io

from PIL import Image
from libxmp import XMPFiles, XMPError
from libxmp import consts as xmpconsts

import logging
import time

LOG = logging.getLogger()

METADATA = [
    {
        'name': 'rating',
        'namespace': xmpconsts.XMP_NS_XMP,
        'attribute': 'xmp:Rating',
        'type': int,
        'default': 0
    }
]


def _metadata_defaults():
    return {meta['name']: meta['default'] for meta in METADATA}


def timing(msg, starttime):
    LOG.debug('%s %f ms', msg, (time.time()-starttime) * 1000)


class Picture(object):
    def __init__(self, filename):
        self.filename = filename
        self.metadata = None
        self.image = None

    def _read_metadata(self):
        self.metadata = XMPFiles(file_path=self.filename).get_xmp()

    def get_metadata(self):
        try:
            if not self.metadata:
                self._read_metadata()
        except XMPError:
            LOG.debug('Error reading xmp metadata for %s', self.filename)
            return _metadata_defaults()

        metadata = {}
        for meta in METADATA:
            try:
                value = self.metadata.get_property(meta['namespace'], meta['attribute'])
                metadata[meta['name']] = meta['type'](value)
            except XMPError:
                metadata[meta['name']] = meta['default']

        return metadata

    def _set_metadata(self, namespace, param, value):
        file = XMPFiles(file_path=self.filename, open_forupdate=True)
        xmp = file.get_xmp()
        xmp.set_property(namespace, param, value)
        if not file.can_put_xmp(xmp):
            raise OSError('Can not write metadata to {}'.format(self.filename))
        file.put_xmp(xmp)
        file.close_file()

    def set_rating(self, rating):
        self._set_metadata(xmpconsts.XMP_NS_XMP, 'xmp:Rating', str(rating))

    def _read_image(self):
        if not self.image:
            self.image = self._load_image()

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

        self.image = self.image.resize((x_target, y_target), Image.ANTIALIAS)
        timing('Image resized in', startt)

    def get_content(self):
        if not self.image:
            self._read_image()
        buf = io.BytesIO()
        self.image.save(buf, format="JPEG")
        content = buf.getvalue()
        buf.close()
        return content

