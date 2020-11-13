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
from dataclasses import dataclass


@dataclass
class FrameControl:
    adr: bool = False
    adr_ack_req: bool = False
    ack: bool = False
    options_length: int = 0

    @classmethod
    def deserialize(cls, frame_ctrl):
        try:
            adr = bool(frame_ctrl & 0b10000000)
            adr_ack_req = bool(frame_ctrl & 0b01000000)
            ack = bool(frame_ctrl & 0b00100000)
            options_length = frame_ctrl & 0b00000111
        except Exception:
            raise TypeError("Corrupted frame control field")

        return cls(adr, adr_ack_req, ack, options_length)
