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

import struct
from dataclasses import dataclass
from enum import IntEnum, unique

GWMP_MESSAGE_FORMAT = ">BHB"
GATEWAY_ADDRESS_FORMAT = ">Q"


@unique
class GwmpMessageType(IntEnum):
    PUSH_DATA = 0x00
    PUSH_ACK = 0x01
    PULL_DATA = 0x02
    PULL_ACK = 0x04
    PULL_RESP = 0x03
    TX_ACK = 0x05

    @classmethod
    def downstream(cls):
        """Messages from Network Server to Gateway"""
        return {cls.PUSH_ACK, cls.PULL_RESP, cls.PULL_ACK}

    def upstream(cls):
        """Messages from Gateway to Network Server"""
        return set(list(cls)) - cls.downstream()


@dataclass
class GwmpMessage:
    version: int
    token: int
    type: GwmpMessageType
    gateway: str
    payload: str

    @classmethod
    def from_gateway_message(cls, data):
        """Build GWMP message"""
        size = struct.calcsize(GWMP_MESSAGE_FORMAT)
        version, token, gwmp_type = struct.unpack(GWMP_MESSAGE_FORMAT, data[:size])
        if gwmp_type in GwmpMessageType.downstream():
            gateway = 0
        else:
            gateway = struct.unpack(GATEWAY_ADDRESS_FORMAT, data[size: size + 8])[0]
        payload = data[size + 8:]
        return cls(version, token, gwmp_type, gateway, payload)

    def get_ack(self):
        if self.type == self.PUSH_DATA:
            ack_type = self.PULL_ACK
        elif self.type == self.PUSH_DATA:
            ack_type = self.PULL_ACK
        else:
            raise RuntimeError
        return struct.pack(GWMP_MESSAGE_FORMAT, self.version, self.token, ack_type)

    def get_gateway(self):
        return str(hex(self.gateway))
