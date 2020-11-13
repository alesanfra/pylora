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

import asyncio
import logging

from .application import LoraNetworkServer


def start_network_server():
    loop = asyncio.get_event_loop()
    logger = logging.getLogger('LoRaWAN')
    logger.info("Starting UDP server")

    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(lambda: LoraNetworkServer(), local_addr=('127.0.0.1', 9999))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.warning("Shutdown LoRaWAN network server")

    transport.close()
    loop.close()


if __name__ == "__main__":
    start_network_server()
