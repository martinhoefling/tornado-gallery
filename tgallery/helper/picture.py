from __future__ import division
import StringIO

from PIL.ExifTags import TAGS
from PIL import Image
import pyexiv2


TAGS[0x4746] = 'Rating'
TAGS[0x4749] = 'RatingPercent'
TAGS[0xc4a5] = 'PrintImageMatching'
TAGS[0x000b] = 'ProcessingSoftware'


class Picture(object):
    def __init__(self, filename):
        self.filename = filename
        self.metadata = None
        self.image = None

    def _read_metadata(self):
        self.metadata = pyexiv2.ImageMetadata(self.filename)
        self.metadata.read()

    def get_metadata(self):
        if not self.metadata:
            self._read_metadata()
        meta_keys = self.metadata.exif_keys + self.metadata.iptc_keys + self.metadata.xmp_keys
        return {key: self.metadata[key].raw_value for key in meta_keys}

    def _read_image(self):
        self.image = Image.open(self.filename)
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
        buf = StringIO.StringIO()
        self.image.save(buf, format="JPEG")
        content = buf.getvalue()
        buf.close()
        return content
