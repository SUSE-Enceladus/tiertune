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
from tiertune.defaults import write_state_file
from tiertune.instance_type.base import InstanceTypeBase


class SysCtl:
    """
    **Implements sysctl interface**
    """

    def __init__(self) -> None:
        self._set_called = False

    def __enter__(self) -> 'SysCtl':
        self._set_called = False
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        if exc_type is None and self._set_called:
            write_state_file()

    def set(self, setting: str) -> None:
        """
        Execute sysctl binary with given setting.
        """
        self._set_called = True
        log.info(f'Apply system setting: {setting}')
        Command.run(['sysctl', '-w', setting])

    @staticmethod
    def apply(
        instance: InstanceTypeBase, config: Dict[str, Dict[str, Dict[str, str]]]
    ) -> None:
        instance_type = instance.get_instance_type()
        if instance_type:
            with SysCtl() as sysctl:
                settings_dict = instance.get_settings(instance_type, config).get(
                    'sysctl', {}
                )
                for key in sorted(settings_dict.keys()):
                    setting = '{}{}'.format(
                        key,
                        f'={settings_dict[key]}' if key in settings_dict else '',
                    )
                    sysctl.set(setting)
