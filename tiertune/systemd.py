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
from tiertune.instance_type.base import InstanceTypeBase
from tiertune.defaults import SYSTEMD_CONF


class SystemD:
    """
    **Implements systemd settings interface**
    """

    @staticmethod
    def set(setting: str) -> None:
        """
        Append systemd settings to an overlay file.
        """
        log.info(f'Set systemd global setting: {setting}')
        with open(SYSTEMD_CONF, 'a') as systemd:
            systemd.write(f'{setting}\n')

    @staticmethod
    def apply(
        instance: InstanceTypeBase, config: Dict[str, Dict[str, Dict[str, str]]]
    ) -> None:
        instance_type = instance.get_instance_type()
        if instance_type:
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
                SystemD.set(setting)
            log.info('Apply systemd settings...')
            Command.run(['systemctl', 'daemon-reload'])
