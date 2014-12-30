from concurrent.futures import ProcessPoolExecutor
import unittest
from unittest.mock import Mock
from nose.tools import assert_equal
from tgallery.helper.process_pool import ProcessPool


def tfunc(a):
    return a


class TestProcessPool(unittest.TestCase):
    def test_pool_initialization(self):
        ProcessPool.init(max_workers=1)
        ppool = ProcessPool.instance()
        assert_equal(type(ppool.pool), ProcessPoolExecutor)

    def test_auto_pool_initialization(self):
        ProcessPool.init()
        ppool = ProcessPool.instance()
        assert_equal(type(ppool.pool), ProcessPoolExecutor)

    def test_submit_passthrough(self):
        ProcessPool.init()
        ppool = ProcessPool.instance()
        ppool.pool.submit = Mock()
        ppool.submit(tfunc, 'a')
        ppool.pool.submit.assert_called_once_with(tfunc, 'a')
