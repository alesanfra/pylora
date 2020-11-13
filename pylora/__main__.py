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
from argparse import ArgumentParser
from os.path import join, dirname

from .server import LoraNetworkServer

DEFAULT_CONFIG = join(dirname(__file__), "..", "conf", "netserver.json")


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("--config", help="JSON configuration", type=str, default=DEFAULT_CONFIG)
    parser.add_argument("-p", "--port", help="UDP listening port", type=int, default=5678)
    args = parser.parse_args()
    return args.port, args.config


def run_network_server(port: int, config_path: str):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("pylora")
    logger.info("Starting UDP server")

    loop = asyncio.get_event_loop()

    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(lambda: LoraNetworkServer(config_path, logger), local_addr=("0.0.0.0", port))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.warning("Shutdown LoRaWAN network server")

    transport.close()
    loop.close()
    logger.warning("Done")


def main():
    port, config_path = parse_arguments()
    run_network_server(port, config_path)


if __name__ == "__main__":
    main()
