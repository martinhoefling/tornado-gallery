import json
import logging
import os
import re

from tornado.web import StaticFileHandler, HTTPError

from tgallery.helper.picture import Picture

LOG = logging.getLogger()

IMAGE_SUFFIX = ('jpeg', 'jpg')
THUMBNAIL_REGEXP = re.compile(r'(.+)/thumbnail/(\d+)x(\d+)$')


class GalleryHandler(StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(GalleryHandler, self).__init__(*args, **kwargs)
        self.x_size = None
        self.y_size = None
        self._thumbnail_content = None

    @property
    def thumbnail(self):
        return self.x_size and True

    def parse_url_path(self, url_path):
        self.x_size = None
        self.y_size = None

        absolute_path = super(GalleryHandler, self).parse_url_path(url_path)
        thumbnail = THUMBNAIL_REGEXP.search(absolute_path)

        # this is not a file but matches thumbnail regexp and thumbnail group match is a file
        if not os.path.exists(absolute_path) and thumbnail and os.path.isfile(
                os.path.join(self.root, thumbnail.groups()[0])):
            absolute_path, x_size, y_size = thumbnail.groups()
            LOG.debug('Thumbnail url for %s x %s size', x_size, y_size)
            self.x_size = int(x_size)
            self.y_size = int(y_size)

        return absolute_path

    def validate_absolute_path(self, root, absolute_path):
        LOG.debug('Validating absolute path %s in root %s', absolute_path, root)
        if os.path.isdir(absolute_path):
            LOG.debug('Is a path')
            root = os.path.abspath(root)
            # os.path.abspath strips a trailing /
            # it needs to be temporarily added back for requests to root/
            if not (absolute_path + os.path.sep).startswith(root):
                raise HTTPError(403, '%s is not in root static directory', self.path)

        else:
            absolute_path = super(GalleryHandler, self).validate_absolute_path(root, absolute_path)
        return absolute_path

    def get_content_type(self):
        if os.path.isdir(self.absolute_path):
            return 'application/json'
        else:
            return super(GalleryHandler, self).get_content_type()

    def get_content_size(self):
        if self.thumbnail:
            return len(self._get_thumbnail_content(self.absolute_path))
        else:
            return super(GalleryHandler, self).get_content_size()

    def _get_thumbnail_content(self, absolute_path):
        if not self._thumbnail_content:
            self._thumbnail_content = self._gen_thumbnail_content(absolute_path)
        return self._thumbnail_content

    def _gen_thumbnail_content(self, absolute_path):
        picture = Picture(absolute_path)
        picture.resize(self.x_size, self.y_size)
        content = picture.get_content()
        return content

    def get_content(self, absolute_path, start=None, end=None):
        if self.thumbnail:
            content = self._get_thumbnail_content(absolute_path)
            start = start or 0
            end = end or len(content)
            LOG.debug('Getting thumbnail content from %d to %d', start, end)
            return content[start:end]

        elif os.path.isdir(absolute_path):
            response = {}
            entries = [(entry, os.path.join(absolute_path, entry)) for entry in os.listdir(absolute_path)]
            response['files'] = [{'name': entry, 'metadata': self._get_metadata(full_entry)}
                                 for entry, full_entry in entries if os.path.isfile(full_entry)]
            response['directories'] = [entry for entry, full_entry in entries if os.path.isdir(full_entry)]
            return json.dumps(response)

        else:
            return StaticFileHandler.get_content(absolute_path, start=start, end=end)

    @classmethod
    def _get_metadata(cls, filename):
        if filename.lower().endswith(IMAGE_SUFFIX):
            return Picture(filename).get_metadata()
        else:
            return 'metadata not supported for this file.'


