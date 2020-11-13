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
import json
from dataclasses import dataclass
from typing import List

import dacite


@dataclass
class DeviceConfig:
    name: str
    net_session_key: str
    app_session_key: str
    app_key: str


@dataclass
class Config:
    devices: List[DeviceConfig]


def load_config_from_path(path) -> Config:
    with open(path, "r") as f:
        data = json.load(f)
    return dacite.from_dict(data_class=Config, data=data)
