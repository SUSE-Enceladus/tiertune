# Copyright (c) 2026 SUSE Software Solutions Germany GmbH.  All rights reserved.
#
# This file is part of tiertune.
#
# tiertune is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tiertune is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tiertune. If not, see <http://www.gnu.org/licenses/>
#
import logging as log
from typing import Dict

from tiertune.command import Command
from tiertune.instance_type.base import InstanceTypeBase


class CPUPower:
    """
    **Implements cpupower settings interface**
    """

    @staticmethod
    def set(key: str, value: str) -> None:
        """
        call cpupower for selected settings.
        """
        if key == 'force_latency' and value:
            log.info(f'Set CPU setting: {key}={value}')
            Command.run(['cpupower', 'idle-set', '--disable-by-latency', value])
        else:
            log.info(
                'Unknown CPU setting: {} with value {}'.format(key, value or '')
            )

    @staticmethod
    def apply(
        instance: InstanceTypeBase, config: Dict[str, Dict[str, Dict[str, str]]]
    ) -> None:
        instance_type = instance.get_instance_type()
        if instance_type:
            settings_dict = instance.get_settings(instance_type, config).get(
                'cpupower', {}
            )
            for key in sorted(settings_dict.keys()):
                CPUPower.set(key, settings_dict.get(key, ''))
