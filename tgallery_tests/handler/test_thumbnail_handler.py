from http.client import NOT_FOUND, OK
from unittest import mock

from nose.tools import assert_equal
from tornado.concurrent import Future
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from tgallery.handler.thumbnail_handler import ThumbnailHandler
from tgallery.services.picture_cache import PictureCache
from tgallery.services.process_pool import ProcessPool


class TestThumbnailHandler(AsyncHTTPTestCase):
    def get_app(self):
        return Application([('/(.+)/thumbnail/([0-9]+)x([0-9]+)', ThumbnailHandler, {'path': '/testdata'})])

    def setUp(self):
        ProcessPool._instance = mock.Mock()
        PictureCache._instance = mock.Mock()
        super(TestThumbnailHandler, self).setUp()

    def tearDown(self):
        ProcessPool._instance = None
        PictureCache._instance = None

    @mock.patch('tgallery.handler.thumbnail_handler.os')
    def test_get_thumbnail_not_found(self, os_mock):
        os_mock.path.isfile.return_value = False
        self.http_client.fetch(self.get_url('/muh.jpg/thumbnail/34x45'), self.stop)
        response = self.wait()
        assert_equal(NOT_FOUND, response.code)

    @mock.patch('tgallery.services.process_pool.ProcessPool._instance.submit')
    @mock.patch('tgallery.handler.thumbnail_handler.os')
    def test_get_thumbnail_uncached(self, os_mock, submit_mock):
        os_mock.path.isfile.return_value = True
        PictureCache.instance().lookup.return_value = None
        future = Future()
        future.set_result('abcd')
        submit_mock.return_value = future
        self.http_client.fetch(self.get_url('/muh.jpg/thumbnail/34x45'), self.stop)
        response = self.wait()
        assert_equal(OK, response.code)
        PictureCache.instance().lookup.assert_called_once_with('/testdata/muh.jpg/thumbnail/34x45')
