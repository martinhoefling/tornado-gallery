import unittest
import os
from unittest.mock import Mock, patch

from nose.tools import assert_raises

from nose.tools import assert_equal
from tornado.web import Application, HTTPError

from tgallery.handler.base_handler import BaseHandler


class TestBaseHandler(unittest.TestCase):
    def setUp(self):
        self.handler = BaseHandler(Application(), Mock(), path='/testdir/muh/../testsubdir')

    def test_valid_path_validates(self):
        assert_equal('/testdir/testsubdir', self.handler.get_validated_absolute_path(''))

    @patch('tgallery.handler.base_handler.os')
    def test_valid_path_validates_and_replaces(self, os_mock):
        os_mock.path.sep = '#'
        os_mock.path.abspath = os.path.abspath
        os_mock.path.join = os.path.join
        assert_equal('/testdir/testsubdir', self.handler.get_validated_absolute_path(''))

    def test_valid_path_rejects_path_traversal(self):
        assert_raises(HTTPError, self.handler.get_validated_absolute_path, '..')

    def test_valid_path_rejects_root_path(self):
        assert_raises(HTTPError, self.handler.get_validated_absolute_path, '/')
