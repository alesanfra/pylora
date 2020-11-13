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
from asyncio import DatagramTransport
from logging import Logger
from typing import List

from pylora.config import DeviceConfig
from pylora.entity.message.gwmp import GwmpMessage, GwmpMessageType
from pylora.entity.message.lorawan import LorawanMessage
from pylora.entity.message.lorawan.data import LorawanDataMessage


class GatewayMessageHandler:
    def __init__(self, logger: Logger, devices: List[DeviceConfig]):
        self.logger: Logger = logger
        self.devices: List[DeviceConfig] = devices
        self.gateways = {}

    def __call__(self, transport: DatagramTransport, message, gateway_address):
        gm = GwmpMessage.from_gateway_message(message)

        if gm.type == GwmpMessageType.PUSH_DATA:
            self.logger.info("PUSH_DATA received")
            transport.sendto(gm.get_ack(), gateway_address)  # send PUSH_ACK
            payload = json.loads(gm.payload)

            for message in payload.get("rxpk", []):
                lorawan_message = LorawanMessage.deserialize(message["data"])

                if isinstance(lorawan_message, LorawanDataMessage):
                    self.handle_lorawan_message(lorawan_message)
                else:
                    raise TypeError("LoRaWAN message type unknown")

        elif gm.type == GwmpMessageType.PULL_DATA:
            self.logger.info("PULL_DATA received")
            transport.sendto(gm.get_ack(), gateway_address)  # send PULL_ACK
            self.gateways[gm.gateway] = gateway_address  # save address for PULL_RESP

        elif gm.type == GwmpMessageType.TX_ACK:
            self.logger.info("TX_ACK received")
        else:
            raise TypeError("GWMP message type unknown")

    def handle_lorawan_message(self, lorawan_message):
        self.logger.info("Handle message {}".format(lorawan_message.payload))
        # elif mm.type == MacMessage.UNCONFIRMED_DATA_UP:
        # print
        # "Message type: UNCONFIRMED DATA UP"
        # frame = FrameMessage(mm.payload)
        # decrypted = frame.decrypt(APP_SESSION_KEY)
        # print
        # "Decrypted payload", array.array('B', decrypted)
        #
        # elif mm.type == MacMessage.CONFIRMED_DATA_UP:
        # print
        # "Message type: CONFIRMED DATA UP"
