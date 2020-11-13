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


class Device:
    CONFIGURATION_FIELDS = ("dev_addr", "dev_eui", "app_eui", "app_key", "net_session_key", "app_session_key", "name")

    def __init__(
        self,
        dev_addr=None,
        dev_eui=None,
        app_eui=None,
        app_key=None,
        net_session_key=None,
        app_session_key=None,
        name=None,
    ):
        self.dev_addr = dev_addr
        self.dev_eui = dev_eui
        self.app_eui = app_eui
        self.app_key = app_key
        self.net_session_key = net_session_key
        self.app_session_key = app_session_key
        self.name = name

    @classmethod
    def from_configuration_json(cls, config):
        return cls(**{field: config.get(field) for field in cls.CONFIGURATION_FIELDS})
