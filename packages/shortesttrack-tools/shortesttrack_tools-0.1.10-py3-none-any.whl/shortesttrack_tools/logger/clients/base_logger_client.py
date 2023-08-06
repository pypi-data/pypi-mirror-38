import abc

import six


@six.add_metaclass(abc.ABCMeta)
class BaseLoggerClient:
    def __init__(self, *args, **kwargs):
        from shortesttrack_tools.logger import getLogger
        self._meta_logger = getLogger('prototype-logger-client.meta-logger')
        self._is_connected = False
        self._id: str = None
        self._token: str = None
        try:
            self._connection_address = self._get_connection_address()
            self._id = self._get_id()
            self._token = self._get_token()
        except Exception as e:
            self._meta_logger.warning(f'Error on getting logger parameters: {e}')

    @abc.abstractmethod
    def send(self, message, level):
        pass

    @abc.abstractmethod
    def _get_connection_address(self):
        pass

    @abc.abstractmethod
    def _get_id(self):
        pass

    @abc.abstractmethod
    def _get_token(self):
        pass
