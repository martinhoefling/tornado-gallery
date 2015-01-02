from http.client import FORBIDDEN
import logging

from tornado.web import RequestHandler, os, HTTPError


LOG = logging.getLogger()


class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        self.root = ''
        super(BaseHandler, self).__init__(*args, **kwargs)

    def initialize(self, path=None):
        self.root = os.path.abspath(path)

    def get_validated_absolute_path(self, path):
        LOG.debug('Validating absolute path %s in root %s', path, self.root)

        abs_path = os.path.abspath(os.path.join(self.root, path))
        # os.path.abspath strips a trailing /
        # it needs to be temporarily added back for requests to root/
        if not (abs_path + os.path.sep).startswith(self.root):
            raise HTTPError(FORBIDDEN, '%s is not in root directory', path)

        return abs_path
