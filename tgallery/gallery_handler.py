import json
import logging
import os
import re

from tornado.web import StaticFileHandler, HTTPError

from tgallery.picture import Picture


app_log = logging.getLogger("tornado.application")

image_suffix = ('jpeg', 'jpg')

thumbnail_regexp = re.compile(r'(.+)/thumbnail/(\d+)x(\d+)$')


class GalleryHandler(StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(GalleryHandler, self).__init__(*args, **kwargs)
        self.x_size = None
        self.y_size = None

    def parse_url_path(self, url_path):
        self.x_size = None
        self.y_size = None

        absolute_path = super(GalleryHandler, self).parse_url_path(url_path)
        thumbnail = thumbnail_regexp.search(absolute_path)

        # this is not a file but matches thumbnail regexp and thumbnail group match is a file
        if not os.path.exists(absolute_path) and thumbnail and os.path.isfile(
                os.path.join(self.root, thumbnail.groups()[0])):
            absolute_path, self.x_size, self.y_size = thumbnail.groups()
            self.x_size = int(self.x_size)
            self.y_size = int(self.y_size)

        return absolute_path

    def validate_absolute_path(self, root, absolute_path):
        if os.path.isdir(absolute_path):
            root = os.path.abspath(root)
            # os.path.abspath strips a trailing /
            # it needs to be temporarily added back for requests to root/
            if not (absolute_path + os.path.sep).startswith(root):
                raise HTTPError(403, "%s is not in root static directory",
                                self.path)

        else:
            absolute_path = super(GalleryHandler, self).validate_absolute_path(root, absolute_path)
        return absolute_path

    def get_content_type(self):
        if os.path.isdir(self.absolute_path):
            return 'application/json'
        else:
            return super(GalleryHandler, self).get_content_type()

    def get_content(self, absolute_path, start=None, end=None):
        if self.x_size and self.y_size:
            picture = Picture(absolute_path)
            picture.resize(self.x_size, self.y_size)
            return picture.get_content()
        elif os.path.isdir(absolute_path):
            response = {}
            entries = [(entry, os.path.join(absolute_path, entry)) for entry in os.listdir(absolute_path)]
            response['files'] = [(entry, self._get_metadata(full_entry))
                                 for entry, full_entry in entries if os.path.isfile(full_entry)]
            response['directories'] = [entry for entry, full_entry in entries if os.path.isdir(full_entry)]
            return json.dumps(response)

        else:
            return StaticFileHandler.get_content(absolute_path, start=start, end=end)

    @classmethod
    def _get_metadata(cls, filename):
        if filename.lower().endswith(image_suffix):
            return Picture(filename).get_metadata()
        else:
            return 'metadata not supported'


