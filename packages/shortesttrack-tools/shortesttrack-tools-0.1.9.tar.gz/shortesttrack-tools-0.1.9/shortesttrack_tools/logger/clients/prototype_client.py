import json
import os
import socket
from datetime import datetime
from typing import Tuple

from pytz import UTC

from shortesttrack_tools.logger.channels import LogChannel
from shortesttrack_tools.logger.clients.base_logger_client import BaseLoggerClient


class PrototypeLoggerClient(BaseLoggerClient):
    def __init__(
            self,
            channel: LogChannel,
            logger_id: str = os.getenv('PROTOTYPE_LOGGER_ID'),
            token: str = os.getenv('PROTOTYPE_LOGGER_TOKEN')
    ):
        self._pre_installed_logger_id = logger_id
        self._pre_installed_token = token
        super().__init__()

        self._channel = channel

        try:
            self._socket = socket.socket()
            self._socket.connect(self._connection_address)
        except Exception as e:
            self._meta_logger.warning(f'Error on socket connection to logger service: {e}')
        else:
            self._is_connected = True

        if self._is_connected:
            self._auth()

    def send(self, message: str, level: str):
        if self._is_connected:
            serialized_message = self._serialize_message(message, level)
            # Send messages only if logger is connected
            try:
                self._socket.sendall(serialized_message)
            except Exception as e:
                self._meta_logger.warning(f'Cannot send message to logger service: {e}')
                self._is_connected = False

    def _get_connection_address(self) -> Tuple[str, int]:
        ip = os.getenv('PROTOTYPE_LOGGER_IP')
        port = int(os.getenv('PROTOTYPE_LOGGER_PORT'))
        assert all([ip, port])
        return ip, port

    def _get_id(self):
        return self._pre_installed_logger_id

    def _get_token(self):
        return self._pre_installed_token

    def __del__(self):
        self._socket.close()

    def _serialize_message(self, message: str, level: str) -> bytes:
        json_message = json.dumps({
            'log_id': self._id,
            'ts': str(datetime.now().astimezone(UTC).isoformat()),
            'ch': self._channel,
            'msg': message,
            'lvl': level
        })

        json_message += '\n'

        return json_message.encode()

    def _auth(self):
        token_bytes = f'{self._token}\n'.encode()
        try:
            self._socket.sendall(token_bytes)
        except Exception as e:
            self._meta_logger.warning(f'Cannot send auth message to logger service: {e}')
