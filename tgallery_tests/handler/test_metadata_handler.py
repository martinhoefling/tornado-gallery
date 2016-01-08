from http.client import NOT_FOUND, OK
import json
from unittest import mock

from nose.tools import assert_equal
from tornado.httpclient import HTTPRequest
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from tgallery.handler.metadata_handler import MetadataHandler


class TestMetadataHandler(AsyncHTTPTestCase):
    @staticmethod
    def get_app():
        return Application([('/(.*)', MetadataHandler, {'path': '/testdata'})])

    @mock.patch('tgallery.handler.metadata_handler.os')
    def test_set_metadata_not_found(self, os_mock):
        os_mock.path.isdir.return_value = False
        os_mock.path.isfile.return_value = False
        self.http_client.fetch(HTTPRequest(self.get_url('/muh.jpg'),
                                           method='PUT',
                                           body=json.dumps({'rating': 4})),
                               self.stop)
        response = self.wait()
        assert_equal(NOT_FOUND, response.code)

    @mock.patch('tgallery.util.picture.Picture.set_metadata')
    @mock.patch('tgallery.handler.metadata_handler.os')
    def test_set_metadata_gallery(self, os_mock, picture_set_metadata_mock):
        os_mock.path.isdir.return_value = False
        os_mock.path.isfile.return_value = True

        self.http_client.fetch(HTTPRequest(self.get_url('/muh.jpg'),
                                           method='PUT',
                                           body=json.dumps({'rating': 4})),
                               self.stop)
        response = self.wait()
        picture_set_metadata_mock.assert_called_once_with({'rating': 4})
        assert_equal(OK, response.code)
