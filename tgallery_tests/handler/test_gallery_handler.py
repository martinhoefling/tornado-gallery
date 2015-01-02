from http.client import NOT_FOUND, OK
import json
from unittest import mock
import unittest
import os
from unittest.mock import Mock

from nose.tools import assert_equal
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from tgallery.handler.gallery_handler import GalleryHandler, NO_METADATA_MSG


class TestGalleryHandler(AsyncHTTPTestCase):
    def get_app(self):
        return Application([('/(.*)', GalleryHandler, {'path': '/testdata'})])

    @mock.patch('tgallery.handler.gallery_handler.GalleryHandler._get_content')
    @mock.patch('tgallery.handler.gallery_handler.os')
    def test_get_gallery_not_found(self, os_mock, get_content_mock):
        get_content_mock.return_value = 'jpegdata'
        os_mock.path.sep = '/'
        os_mock.path.isdir.return_value = False
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()
        assert_equal(NOT_FOUND, response.code)

    @mock.patch('tgallery.handler.gallery_handler.GalleryHandler._get_content')
    @mock.patch('tgallery.handler.gallery_handler.os')
    def test_get_gallery_found(self, os_mock, get_content_mock):
        get_content_mock.return_value = 'jpegdata'
        os_mock.path.sep = '/'
        os_mock.path.isdir.return_value = True
        self.http_client.fetch(self.get_url('/muh'), self.stop)
        response = self.wait()
        assert_equal(OK, response.code)
        assert_equal(b'jpegdata', response.body)
        get_content_mock.assert_called_once_with('/testdata/muh')

    @mock.patch('tgallery.handler.gallery_handler.GalleryHandler._get_content')
    @mock.patch('tgallery.handler.gallery_handler.os')
    def test_get_gallery_rewrites_separators(self, os_mock, get_content_mock):
        get_content_mock.return_value = 'jpegdata'
        os_mock.path.sep = '#'
        os_mock.path.isdir.return_value = True
        self.http_client.fetch(self.get_url('/muh/maeh'), self.stop)
        response = self.wait()
        assert_equal(OK, response.code)
        assert_equal(b'jpegdata', response.body)
        get_content_mock.assert_called_once_with('/testdata/muh#maeh')


class TestGalleryHandlerGetContent(unittest.TestCase):
    def setUp(self):
        self.handler = GalleryHandler(Application(), Mock(), path='/testdir/muh/../testsubdir')

    @mock.patch('tgallery.handler.gallery_handler.os')
    def test_get_content_gets_directories(self, os_mock):
        os_mock.path.join = os.path.join
        os_mock.path.isdir.return_value = True
        os_mock.path.isfile.return_value = False
        os_mock.listdir.return_value = ['maeh']
        assert_equal({'files': [], 'directories': ['maeh']},
                     json.loads(self.handler._get_content('/miau')))

    @mock.patch('tgallery.handler.gallery_handler.os')
    def test_get_content_gets_any_file(self, os_mock):
        os_mock.path.join = os.path.join
        os_mock.path.isdir.return_value = False
        os_mock.path.isfile.return_value = True
        os_mock.listdir.return_value = ['maeh.txt']
        assert_equal({'files': [{'name': 'maeh.txt', 'metadata': NO_METADATA_MSG}], 'directories': []},
                     json.loads(self.handler._get_content('/miau')))

    @mock.patch('tgallery.util.picture.Picture.get_metadata')
    @mock.patch('tgallery.handler.gallery_handler.os')
    def test_get_content_gets_image_file(self, os_mock, picture_metadata_mock):
        picture_metadata_mock.return_value = 'somemeta'
        os_mock.path.join = os.path.join
        os_mock.path.isdir.return_value = False
        os_mock.path.isfile.return_value = True
        os_mock.listdir.return_value = ['maeh.JPG']
        assert_equal({'files': [{'name': 'maeh.JPG', 'metadata': 'somemeta'}], 'directories': []},
                     json.loads(self.handler._get_content('/miau')))

