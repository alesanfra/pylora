"""
This file is part of PyLora.

PyLora is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyLora is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyLora. If not, see <http://www.gnu.org/licenses/>.
"""

import logging
from asyncio import DatagramProtocol, BaseTransport, DatagramTransport

from .config import load_config_from_path
from .handler.gateway import GatewayMessageHandler


class LoraNetworkServer(DatagramProtocol):
    def __init__(self, config_path: str, logger: logging.Logger):
        self.logger = logger
        self.configuration = load_config_from_path(config_path)
        self.gateway_handler = GatewayMessageHandler(self.logger, self.configuration.devices)
        self.transport = None

    def connection_made(self, transport: DatagramTransport):
        self.transport = transport
        self.logger.info(f"Network Server listening")

    def datagram_received(self, data, address):
        try:
            self.logger.info(f"Received message from {address}")
            self.gateway_handler(self.transport, data.decode(), address)
        except Exception as e:
            self.logger.exception(e)
