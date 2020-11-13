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

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms


def cmac_sign(message: bytes, key: bytes) -> bytes:
    c = cmac.CMAC(algorithms.AES(key), backend=default_backend())
    c.update(message)
    return c.finalize()


def cmac_verify(message: bytes, key: bytes, signature: bytes) -> bool:
    c = cmac.CMAC(algorithms.AES(key), backend=default_backend())
    c.update(message)
    try:
        c.verify(signature)
        return True
    except InvalidSignature:
        return False
