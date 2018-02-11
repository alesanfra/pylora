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

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms


def prova_cmac(key):
    c = cmac.CMAC(algorithms.AES(key), backend=default_backend())
    c.update(b"message to authenticate")
    h = c.finalize()
    print(h)

    c = cmac.CMAC(algorithms.AES(key), backend=default_backend())
    c.update(b"message to authenticate")
    # c.verify(h)
    c.verify(b"an incorrect signature")


prova_cmac(b'01020304050607080910111213141516')

logger = logging.getLogger()

logger.warning('ciao')
