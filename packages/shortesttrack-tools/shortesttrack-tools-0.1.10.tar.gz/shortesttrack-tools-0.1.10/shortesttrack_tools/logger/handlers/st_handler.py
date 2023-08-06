from logging import StreamHandler, LogRecord

from shortesttrack_tools.logger.clients.base_logger_client import BaseLoggerClient


class STLoggerHandler(StreamHandler):
    def __init__(self, client: BaseLoggerClient):
        from shortesttrack_tools.logger import getLogger
        self._client = client
        self._meta_logger = getLogger('st-logger-handler.meta-logger')
        super().__init__()

    def emit(self, record: LogRecord):
        message = self.format(record)
        try:
            self._client.send(message, str(record.levelname))
        except Exception as e:
            self._meta_logger.warning(f'Error on sending message to logger service: {e}')
