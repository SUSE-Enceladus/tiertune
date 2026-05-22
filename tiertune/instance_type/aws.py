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

# project
from tiertune.instance_type.base import InstanceTypeBase
from tiertune.command import Command


class InstanceTypeAws(InstanceTypeBase):
    """
    **Implements AWS instance type interface**
    """

    def get_instance_type(self) -> str:
        """
        Implementation in CSP specific InstanceType* class
        """
        metadata = Command.run(['ec2metadata', '--instance-type'])
        return metadata.output.strip() if metadata else ''
