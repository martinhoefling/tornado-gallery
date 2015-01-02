import unittest
from unittest.mock import Mock
from nose.tools import assert_raises
from nose.tools import assert_equal
from tornado.web import Application, HTTPError

from tgallery.handler.base_handler import BaseHandler


class TestBaseHandler(unittest.TestCase):
    def setUp(self):
        self.handler = BaseHandler(Application(), Mock(), path='/testdir/muh/../testsubdir')

    def test_valid_path_validates(self):
        assert_equal('/testdir/testsubdir', self.handler.get_validated_absolute_path(''))

    def test_valid_path_rejects_path_traversal(self):
        assert_raises(HTTPError, self.handler.get_validated_absolute_path, '..')

    def test_valid_path_rejects_root_path(self):
        assert_raises(HTTPError, self.handler.get_validated_absolute_path, '/')
