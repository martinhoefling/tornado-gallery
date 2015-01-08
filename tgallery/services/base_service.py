import logging

LOG = logging.getLogger()


class BaseService(object):
    _instance = None

    @classmethod
    def init(cls, *args, **kwargs):
        cls._instance = cls(*args, **kwargs)
        LOG.info('Service %s initialized', cls.__name__)

    @classmethod
    def instance(cls):
        assert cls._instance, 'Service {} not initialized yet'.format(cls.__name__)
        return cls._instance

    @classmethod
    def initialized(cls):
        return bool(cls._instance)
