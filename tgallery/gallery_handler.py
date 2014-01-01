import json
import logging
import os

from tornado.web import StaticFileHandler, HTTPError
from tornado.util import bytes_type


app_log = logging.getLogger("tornado.application")


class GalleryHandler(StaticFileHandler):
    path = None
    absolute_path = None
    modified = None

    def initialize(self, *args, **kwargs):
        super(GalleryHandler, self).initialize(*args, **kwargs)
        app_log.info('Initializing gallery handler with path {}'.format(kwargs['path']))

    def get(self, path, include_body=True):
        self.path = self.parse_url_path(path)
        absolute_path = self.get_absolute_path(self.root, self.path)
        if os.path.isdir(absolute_path):
            self.get_dir(absolute_path)
        else:
            super(GalleryHandler, self).get(path, include_body=include_body)

    def get_dir(self, absolute_path, include_body=True):
        if not (absolute_path + os.path.sep).startswith(self.root):
            raise HTTPError(403, "%s is not in root gallery directory", self.path)

        self.absolute_path = absolute_path

        self.modified = self.get_modified_time()
        self.set_headers()
        self.set_header('Content-Type', 'application/json')

        if self.should_return_304():
            self.set_status(304)
            return

        content = self.get_dir_content(self.absolute_path)
        if isinstance(content, bytes_type):
            content = [content]
        content_length = 0
        for chunk in content:
            if include_body:
                self.write(chunk)
            else:
                content_length += len(chunk)
        if not include_body:
            assert self.request.method == "HEAD"
            self.set_header("Content-Length", content_length)

    @classmethod
    def get_dir_content(cls, absolute_path):
        response = {}
        entries = [os.path.join(absolute_path, entry) for entry in os.listdir(absolute_path)]
        response['files'] = [entry for entry in entries if os.path.isfile(entry)]
        response['directories'] = [entry for entry in entries if os.path.isdir(entry)]
        return json.dumps(response)
