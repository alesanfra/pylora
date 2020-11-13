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

import json
import logging
from pathlib import Path

from ..handler.gateway import GatewayMessageHandler

CONFIGURATION_FILE = Path(__file__).parent / '..' / '..' / 'conf' / 'netserver.json'


class LoraNetworkServer:
    def __init__(self):
        self.log = logging.getLogger("LoRaWAN")
        self.transport = None
        self.gateway_handler = None
        self.configuration = self.__load_configuration()
        print(self.configuration)

    def connection_made(self, transport):
        self.transport = transport
        self.gateway_handler = GatewayMessageHandler(self.log, self.transport, self.configuration["devices"])
        self.log.info("Network Server listening on {}".format(transport.__dict__))

    def datagram_received(self, data, address):
        try:
            self.log.info("Received message from %s".format(address))
            self.gateway_handler(data.decode(), address)
        except Exception as e:
            self.log.exception(e)

    @staticmethod
    def __load_configuration():
        with open(CONFIGURATION_FILE) as f:
            return json.load(f)
