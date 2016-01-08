from http.client import NOT_FOUND
import json
import logging
import os
import re

from tornado.web import HTTPError

from tgallery.handler.base_handler import BaseHandler
from tgallery.util.picture import Picture


LOG = logging.getLogger()

IMAGE_SUFFIX = ('jpeg', 'jpg')
THUMBNAIL_REGEXP = re.compile(r'(.+)/thumbnail/(\d+)x(\d+)$')

NO_METADATA_MSG = 'metadata not supported for this file.'


class GalleryHandler(BaseHandler):
    def get(self, path):
        abs_path = self.get_validated_absolute_path(path)

        if not os.path.isdir(abs_path):
            raise HTTPError(NOT_FOUND, 'Directory {0} not found'.format(path))

        self.set_header('Content-Type', 'image/jpeg')
        response = self._get_content(abs_path)
        self.write(response)

    def _get_content(self, absolute_path):
        response = {}
        entries = [(entry, os.path.join(absolute_path, entry)) for entry in os.listdir(absolute_path)]
        response['files'] = [{'name': entry, 'metadata': self._get_metadata(full_entry)}
                             for entry, full_entry in entries if os.path.isfile(full_entry)]
        response['directories'] = [entry for entry, full_entry in entries if os.path.isdir(full_entry)]
        return json.dumps(response)

    @staticmethod
    def _get_metadata(filename):
        if filename.lower().endswith(IMAGE_SUFFIX):
            return Picture(filename).get_metadata()
        else:
            return '%s' % NO_METADATA_MSG


