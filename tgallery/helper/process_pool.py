from concurrent.futures import ProcessPoolExecutor
import logging
from tgallery.helper.base_service import BaseService

LOG = logging.getLogger()


class ProcessPool(BaseService):
    _instance = None

    def __init__(self, max_workers=None):
        if max_workers:
            LOG.info('Creating process pool with %d workers', max_workers)
        else:
            LOG.info('Creating process pool with automatic worker count')

        self.pool = ProcessPoolExecutor(max_workers=max_workers)

    def submit(self, fn, *args, **kwargs):
        return self.pool.submit(fn, *args, **kwargs)
