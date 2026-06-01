# Copyright (c) 2026 SUSE Software Solutions Germany GmbH.  All rights reserved.
#
# This file is part of tiertune.
#
# tiertune is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tiertune is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tiertune.  If not, see <http://www.gnu.org/licenses/>
#
import logging as log
import sys

from tiertune.exceptions import TierTuneError
from tiertune.instance_type import InstanceType
from tiertune.config import Config
from tiertune.sysctl import SysCtl


def main() -> None:
    try:
        SysCtl.apply(InstanceType.new('aws'), Config.read_aws())
    except TierTuneError as issue:
        # known exception, log information and exit
        log.error('{}: {}'.format(type(issue).__name__, issue))
        sys.exit(1)
    except Exception:
        # exception we did not expect, show python backtrace
        log.error('Unexpected error:')
        raise
