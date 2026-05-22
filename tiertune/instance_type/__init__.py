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
import importlib
from abc import ABCMeta, abstractmethod

from tiertune.exceptions import TierTuneInstanceTypeError


class InstanceType(metaclass=ABCMeta):
    """
    **InstanceType factory
    """

    @abstractmethod
    def __init__(self) -> None:
        return None  # pragma: no cover

    @staticmethod
    def new(csp_name: str):
        name_map = {
            'gce': ['gce', 'Gce'],
            'azure': ['azure', 'Azure'],
            'aws': ['aws', 'Aws'],
        }
        try:
            module_namespace, module_name = name_map[csp_name]
            csp = importlib.import_module(
                'tiertune.instance_type.{0}'.format(module_namespace)
            )
            module_name = 'InstanceType{0}'.format(module_name)
            csp_instance = csp.__dict__[module_name]()
        except Exception as issue:
            raise TierTuneInstanceTypeError(
                'Support for CSP {0} not implemented {1}'.format(
                    csp_name, issue
                )
            )
        return csp_instance
