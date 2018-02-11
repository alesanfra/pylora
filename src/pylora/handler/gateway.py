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

from pylora.entity.message.gwmp import GWMPMessage
from pylora.entity.message.lorawan import LorawanMessage
from pylora.entity.message.lorawan.data import LorawanDataMessage

BUFF_LEN = 2408

gateways = {}


class GatewayMessageHandler:
    def __init__(self, log, transport, devices):
        self.log = log
        self.transport = transport
        self.devices = devices

    def __call__(self, message, gateway_address):
        gm = GWMPMessage.from_gateway_message(message)

        if gm.type == GWMPMessage.PUSH_DATA:
            self.log.info("PUSH_DATA received")
            self.transport.sendto(gm.get_ack(), gateway_address)  # send PUSH_ACK
            payload = json.loads(gm.payload)

            for message in payload.get("rxpk", []):
                lorawan_message = LorawanMessage.deserialize(message['data'])

                if isinstance(lorawan_message, LorawanDataMessage):
                    self.handle_lorawan_message(lorawan_message)
                else:
                    raise TypeError("LoRaWAN message type unknown")

        elif gm.type == GWMPMessage.PULL_DATA:
            self.log.info("PULL_DATA received")
            self.transport.sendto(gm.get_ack(), gateway_address)  # send PULL_ACK
            global gateways
            gateways[gm.gateway] = self.transport  # save address for PULL_RESP

        elif gm.type == GWMPMessage.TX_ACK:
            self.log.info("TX_ACK received")
        else:
            raise TypeError("GWMP message type unknown")

    def handle_lorawan_message(self, lorawan_message):
        self.log.info("Handle message {}".format(lorawan_message.payload))
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
