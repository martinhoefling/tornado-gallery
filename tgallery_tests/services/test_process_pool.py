from concurrent.futures import ProcessPoolExecutor
import unittest
from unittest.mock import Mock

from nose.tools import assert_equal

from tgallery.services.process_pool import ProcessPool


def tfunc(a):
    return a


class TestProcessPool(unittest.TestCase):
    @staticmethod
    def test_pool_initialization():
        ProcessPool.init(max_workers=1)
        ppool = ProcessPool.instance()
        assert_equal(type(ppool.pool), ProcessPoolExecutor)

    @staticmethod
    def test_auto_pool_initialization():
        ProcessPool.init()
        ppool = ProcessPool.instance()
        assert_equal(type(ppool.pool), ProcessPoolExecutor)

    @staticmethod
    def test_submit_passthrough():
        ProcessPool.init()
        ppool = ProcessPool.instance()
        ppool.pool.submit = Mock()
        ppool.submit(tfunc, 'a')
        ppool.pool.submit.assert_called_once_with(tfunc, 'a')
