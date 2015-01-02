from http.client import NOT_FOUND
import json
import logging
import os

from tornado.web import HTTPError

from tgallery.handler.base_handler import BaseHandler
from tgallery.util.picture import Picture


LOG = logging.getLogger()


class MetadataHandler(BaseHandler):
    def put(self, filepath):
        metadata = json.loads(str(self.request.body.decode()))

        if os.path.sep != "/":
            filepath = filepath.replace("/", os.path.sep)

        abs_path = self.get_validated_absolute_path(filepath)

        if not os.path.isfile(abs_path):
            raise HTTPError(NOT_FOUND, 'File {} not found'.format(filepath))

        picture = Picture(abs_path)
        picture.set_metadata(metadata)
        self.finish()
