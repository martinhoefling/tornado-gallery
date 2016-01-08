import unittest

from nose.tools import assert_true, assert_false, assert_raises

from tgallery.services.base_service import BaseService


class AService(BaseService):
    _instance = None

    def __init__(self):
        pass


class AnotherService(BaseService):
    _instance = None

    def __init__(self):
        pass


class TestBaseService(unittest.TestCase):
    @staticmethod
    def test_init_separate_services():
        assert_false(AService.initialized())
        assert_false(AnotherService.initialized())
        assert_raises(AssertionError, AService.instance)
        assert_raises(AssertionError, AnotherService.instance)

        AService.init()
        assert_true(AService.initialized())
        assert_false(AnotherService.initialized())

        AnotherService.init()
        assert_true(AService.initialized())
        assert_true(AnotherService.initialized())
        assert_true(AService.instance())
        assert_true(AnotherService.instance())
