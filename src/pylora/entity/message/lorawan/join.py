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

# import base64
# import json
# import struct
# from collections import OrderedDict
#
# from pylora.entity.message.lorawan import LorawanMessage, JOIN_ACCEPT_DELAY1, MAX_TMST
#
#
# class JoinRequestMessage(LorawanMessage):
#     def __init__(self, type=None, version=None, mic=None, app_eui=None, dev_eui=None, dev_nonce=None):
#         super().__init__(type, version, mic)
#         self.app_eui = app_eui
#         self.dev_eui = dev_eui
#         self.dev_nonce = dev_nonce
#
#     @classmethod
#     def deserialize_frame_layer(cls, type, version, payload, mic):
#         app_eui, dev_eui, dev_nonce = struct.unpack("<QQH", payload)  # Little Endian
#         return cls(type=type, version=version, mic=mic, app_eui=app_eui, dev_eui=dev_eui, dev_nonce=dev_nonce, )
#
#     def build_join_accept(self, msg):
#         # Build JOIN_ACCEPT
#         ja_data = struct.pack("<BBHBHLBB", self.JOIN_ACCEPT << 5, 1, 2, 3, 4, 10, 0, 0)
#         mic = self.compute_mic(APP_KEY, ja_data)
#         ja_data = struct.pack("<BBHBHLBBL", self.JOIN_ACCEPT << 5, 1, 2, 3, 4, 10, 0, 0, mic)  # Build JOIN_ACCEPT
#         # deve essere cifrato!
#
#         # Build JOIN_ACCEPT
#         txpk = OrderedDict()
#         txpk['tmst'] = (msg['tmst'] + JOIN_ACCEPT_DELAY1) % MAX_TMST
#         txpk['freq'] = msg['freq']
#         txpk['rfch'] = msg['rfch']
#         txpk['powe'] = 14
#         txpk['modu'] = msg['modu']
#         txpk['datr'] = msg['datr']
#         txpk['codr'] = msg['codr']
#         txpk['size'] = len(ja_data)
#         txpk['data'] = base64.urlsafe_b64encode(ja_data)
#         join_accept = {'txpk': txpk}
#         return json.dumps(join_accept, separators=(',', ':'))
#
#
# class JoinAcceptMessage(LorawanMessage):
#     @classmethod
#     def deserialize_frame_layer(cls, type, version, payload, mic):
#         raise RuntimeError
