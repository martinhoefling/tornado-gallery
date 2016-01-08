import io
import logging
import time

from PIL import Image
from libxmp import XMPFiles, XMPError
from libxmp import consts as xmpconsts

LOG = logging.getLogger()

METADATA = {
    'rating': {
        'namespace': xmpconsts.XMP_NS_XMP,
        'attribute': 'xmp:Rating',
        'type': int,
        'default': 0
    }
}


class MetadataWriteException(Exception):
    pass


def _metadata_defaults():
    return {name: metadict['default'] for name, metadict in METADATA.items()}


def timing(msg, starttime):
    LOG.debug('%s %f ms', msg, (time.time() - starttime) * 1000)


class Picture(object):
    def __init__(self, filename):
        self.filename = filename
        self.metadata = None
        self._image = None

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
        for name, metadict in METADATA.items():
            try:
                value = self.metadata.get_property(metadict['namespace'], metadict['attribute'])
                metadata[name] = metadict['type'](value)
            except XMPError:
                metadata[name] = metadict['default']

        return metadata

    def set_metadata(self, metadata):
        try:
            file = XMPFiles(file_path=self.filename, open_forupdate=True)
            xmp = file.get_xmp()
            for name, value in metadata.items():
                metadict = METADATA[name]
                xmp.set_property(metadict['namespace'], metadict['attribute'], str(value))

            if not file.can_put_xmp(xmp):
                raise MetadataWriteException('Can not write metadata')
            file.put_xmp(xmp)
            file.close_file()

        except XMPError:
            LOG.debug('writing metadata for {0} failed'.format(self.filename))
            raise MetadataWriteException('Writing metadata failed.')

    def _read_image(self):
        if not self._image:
            self._image = self._load_image()

    def _load_image(self):
        startt = time.time()
        try:
            image = Image.open(self.filename)
        except OSError:
            image = Image.new('RGB', (800, 800), 'white')
        image.load()
        timing('Image read in', startt)
        return image

    def resize(self, x_size, y_size):
        if not self._image:
            self._read_image()

        startt = time.time()

        aspect_ratio = self._image.size[0] / self._image.size[1]

        x_target, y_target = self._image.size
        if x_size < x_target:
            x_target = x_size
            y_target = int(x_target / aspect_ratio)
        if y_size < y_target:
            y_target = y_size
            x_target = int(y_target * aspect_ratio)

        if x_target == 0 or y_target == 0:
            x_target = 1
            y_target = 1

        self._image = self._image.resize((x_target, y_target), Image.ANTIALIAS)
        timing('Image resized in', startt)

    def get_content(self):
        if not self._image:
            self._read_image()
        buf = io.BytesIO()
        self._image.save(buf, format="JPEG")
        content = buf.getvalue()
        buf.close()
        return content

