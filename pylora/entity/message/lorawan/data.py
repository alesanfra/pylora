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

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import ECB

from pylora.entity.message.lorawan import LorawanMessage, FrameControl
from pylora.util import key_string_to_bytes, compute_encryption_vector, xor_bytes


@LorawanMessage.implements(LorawanMessage.UNCONFIRMED_DATA_UP,
                           LorawanMessage.UNCONFIRMED_DATA_DOWN,
                           LorawanMessage.CONFIRMED_DATA_UP,
                           LorawanMessage.CONFIRMED_DATA_DOWN)
class LorawanDataMessage(LorawanMessage):
    def __init__(self,
                 lorawan_type=None,
                 version=None,
                 mic=None,
                 address=None,
                 counter=None,
                 control=None,
                 options=None,
                 port=None,
                 payload=None):
        super().__init__(lorawan_type, version, mic)
        self.address: str = address
        self.counter: int = counter
        self.control: FrameControl = control  # declared in frame_control field
        self.options: str = options
        self.port: int = port
        self.payload: str = payload

    @classmethod
    def deserialize_frame_layer(cls, lorawan_type, version, data, mic):
        dev_address, frame_ctrl, frame_cnt = struct.unpack("<LBH", data[:7])
        frame_ctrl = FrameControl.deserialize(frame_ctrl)
        options = data[7:frame_ctrl.options_len] if frame_ctrl.options_len > 0 else ""

        if len(data[7 + frame_ctrl.options_len:]) > 0:
            port = ord(data[7 + frame_ctrl.options_len])
            payload = data[8 + frame_ctrl.options_len:]
        else:
            port = -1
            payload = ""

        return cls(lorawan_type, version, mic, dev_address, frame_cnt, frame_ctrl, options, port, payload)

    def encrypt(self, key_string):
        data = self.payload
        key = key_string_to_bytes(key_string)

        data += b"\0" * (AES.block_size - len(data) % AES.block_size)  # add padding
        cypher = Cipher(AES(key), ECB(), backend=default_backend()).encryptor()

        vector = compute_encryption_vector(len(data), self.address, self.counter)
        s = cypher.update(vector) + cypher.finalize()

        return xor_bytes(data, s)

    def decrypt(self, key):
        return self.encrypt(key)

    def serialize(self, key):
        """
        :type key: str
        :rtype: str
        """
