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

import base64

from pylora.entity.message.lorawan.frame_control import FrameControl

JOIN_ACCEPT_DELAY1 = 5000000  # 5 million microseconds (5 seconds)
MAX_TMST = 0x100000000  # 2^32


class LorawanMessage:
    JOIN_REQUEST = 0b000
    JOIN_ACCEPT = 0b001
    UNCONFIRMED_DATA_UP = 0b010
    UNCONFIRMED_DATA_DOWN = 0b011
    CONFIRMED_DATA_UP = 0b100
    CONFIRMED_DATA_DOWN = 0b101
    LORAWAN_VERSION_1 = 0

    __type_to_subclass__ = {}

    def __init__(self, lorawan_type, version, mic):
        self.lorawan_type = lorawan_type
        self.version = version
        self.mic = mic

    @classmethod
    def deserialize(cls, data):
        lorawan_type, lorawan_version, payload, mic = cls.__deserialize_mac_layer(data)
        subclass = cls.subclass_from_type(lorawan_type)
        return subclass.deserialize_frame_layer(lorawan_type, lorawan_version, payload, mic)

    @classmethod
    def __deserialize_mac_layer(cls, data):
        data = str(data)
        data += b'=' * (4 - len(data) % 4)  # add padding to be multiple of 4
        res = base64.urlsafe_b64decode(data)
        mac_header = ord(res[0])
        type = (mac_header & 0b11100000) >> 5
        lorawan_version = mac_header & 0b00000011
        payload = res[1:len(res) - 4]
        mic = res[len(res) - 4:]
        return type, lorawan_version, payload, mic

    @classmethod
    def deserialize_frame_layer(cls, type, version, payload, mic):
        raise NotImplementedError()

    @classmethod
    def subclass_from_type(cls, lorawan_type):
        try:
            return cls.__type_to_subclass__[lorawan_type]
        except KeyError:
            raise TypeError("Unknown type {}".format(lorawan_type))

    @staticmethod
    def implements(*lorawan_types):
        def wrapper(cls):
            for lorawan_type in lorawan_types:
                LorawanMessage.__type_to_subclass__[lorawan_type] = cls
            return cls

        return wrapper

    @staticmethod
    def __compute_mic(key, data):
        cmac = CMAC.new(key, ciphermod=AES)
        cmac.update(data)
        return int(cmac.hexdigest()[:8], 16)
