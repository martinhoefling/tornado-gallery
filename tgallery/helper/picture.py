from __future__ import division
import io

from PIL import Image
from libxmp import XMPFiles, XMPError
from libxmp import consts as xmpconsts

import logging

LOG = logging.getLogger()


class Picture(object):
    def __init__(self, filename):
        self.filename = filename
        self.metadata = None
        self.image = None

    def _read_metadata(self):
        try:
            self.metadata = XMPFiles(file_path=self.filename).get_xmp()
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
        try:
            self.image = Image.open(self.filename)
        except OSError:
            self.image = Image.new('RGB', (800, 800), 'white')
        self.image.load()

    def resize(self, x_size, y_size):
        if not self.image:
            self._read_image()

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

    def get_content(self):
        if not self.image:
            self._read_image()
        buf = io.BytesIO()
        self.image.save(buf, format="JPEG")
        content = buf.getvalue()
        buf.close()
        return content
