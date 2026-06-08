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


class TuneD:
    """
    **Implements tuned interface**
    """

    @staticmethod
    def set(profile: str) -> None:
        """
        Execute tuned-adm with given profile
        """
        log.info(f'Apply tuned profile: {profile}')
        Command.run(['tuned-adm', 'profile', profile])

    @staticmethod
    def apply(
        instance: InstanceTypeBase, config: Dict[str, Dict[str, Dict[str, str]]]
    ) -> None:
        instance_type = instance.get_instance_type()
        if instance_type:
            settings_dict = instance.get_settings(instance_type, config).get(
                'tuned', {}
            )
            profile = settings_dict.get('profile')
            if profile:
                TuneD.set(profile)
