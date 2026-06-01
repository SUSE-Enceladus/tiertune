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
import re


class InstanceTypeBase:
    """
    **Implements base class for instance type interface**
    """

    def get_instance_type(self) -> str:
        """
        Implementation in CSP specific InstanceType* class
        """
        raise NotImplementedError

    def get_settings(
        self, instance_type: str, config: Dict[str, Dict[str, Dict[str, str]]]
    ) -> Dict[str, Dict[str, str]]:
        """
        Evaluate settings for given instance_type and config
        """
        result: Dict[str, Dict[str, str]] = {}
        log.info('Lookup config settings for instance type: {instance_type}')
        for type_pattern in config.keys():
            if re.match(type_pattern, instance_type):
                log.info('Found matching entry: {type_pattern}')
                result.update(config[type_pattern])
        if result:
            log.info('Using settings dict: {result}')
        return result
