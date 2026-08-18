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

import time

# project
from tiertune.instance_type.base import InstanceTypeBase
from tiertune.command import Command


class InstanceTypeGce(InstanceTypeBase):
    """
    **Implements GCE instance type interface**
    """

    def get_instance_type(self) -> str:
        """
        Use gcemetadata to retrieve instance type name
        """
        # Wait up to 10 minutes for the metadata server to become available
        rem_wait_time = 600
        sleep_time = 180
        wait_cnt = 1
        metadata = ''
        while rem_wait_time > 0:
            metadata = Command.run(
                ['gcemetadata', '--query', 'instance', '--machine-type'],
                raise_on_error=False,
            )
            if metadata.returncode != 0:
                rem_wait_time -= sleep_time
                if rem_wait_time > 0:
                    time.sleep(sleep_time)
                    sleep_time -= wait_cnt * 30
            else:
                rem_wait_time = -1

        return metadata.output.strip() if metadata else ''
