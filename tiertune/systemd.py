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
import os
from typing import Dict

from tiertune.command import Command
from tiertune.defaults import SYSTEMD_CONF
from tiertune.defaults import write_state_file
from tiertune.instance_type.base import InstanceTypeBase


class SystemD:
    """
    **Implements systemd settings interface**
    """

    def __init__(self) -> None:
        self._set_called = False

    def __enter__(self) -> 'SystemD':
        self._set_called = False
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        if exc_type is None and self._set_called:
            write_state_file()

    def set(self, setting: str) -> None:
        """
        Append systemd settings to an overlay file.
        """
        self._set_called = True
        log.info(f'Set systemd global setting: {setting}')
        with open(SYSTEMD_CONF, 'a') as systemd:
            systemd.write(f'{setting}\n')

    @staticmethod
    def apply(
        instance: InstanceTypeBase, config: Dict[str, Dict[str, Dict[str, str]]]
    ) -> None:
        instance_type = instance.get_instance_type()
        if instance_type:
            with SystemD() as systemd:
                if os.path.exists(SYSTEMD_CONF):
                    os.unlink(SYSTEMD_CONF)
                settings_dict = instance.get_settings(instance_type, config).get(
                    'systemd', {}
                )
                for key in sorted(settings_dict.keys()):
                    setting = '{}{}'.format(
                        key,
                        f'={settings_dict[key]}' if key in settings_dict else '',
                    )
                    systemd.set(setting)
                log.info('Apply systemd settings...')
                Command.run(['systemctl', 'daemon-reload'])
