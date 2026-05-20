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


class TierTuneError(Exception):
    """
    **Base class to handle all known exceptions**

    Specific exceptions are implemented as sub classes of TierTuneError

    Attributes

    :param string message: Exception message text
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return format(self.message)


class TierTuneCommandError(TierTuneError):
    """
    Exception raised if an external command called via a Command
    instance has returned with an exit code != 0 or could not
    be called at all.
    """


class TierTuneCommandNotFound(TierTuneError):
    """
    Exception raised if any executable command cannot be found in
    the evironment PATH variable.
    """


class TierTuneDecodingError(TierTuneError):
    """
    Exception is raised on decoding literals failure
    """
