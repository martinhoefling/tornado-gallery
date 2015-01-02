import unittest
from nose.tools import assert_equal, assert_true
import time
from tgallery.services.picture_cache import PictureCache


class TestPictureCache(unittest.TestCase):
    def setUp(self):
        PictureCache.init()
        self.cache = PictureCache.instance()

    def test_store_and_lookup(self):
        self.cache.store('abcd', '1234')
        assert_equal('1234', self.cache.lookup('abcd'))

    def test_invalid_lookup(self):
        assert_equal(None, self.cache.lookup('defg'))

    def test_lookup_time_update(self):
        self.cache.store('abcd', '1234')
        storetime = self.cache._cached_pictures['abcd']['timestamp']
        time.sleep(0.001)
        self.cache.lookup('abcd')
        lookuptime = self.cache._cached_pictures['abcd']['timestamp']
        assert_true(lookuptime > storetime)
