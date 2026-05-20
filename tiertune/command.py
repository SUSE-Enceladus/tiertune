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
import shutil
import os
import subprocess

from typing import List, MutableMapping, NamedTuple, Optional

# project
from tiertune.codec import Codec
from tiertune.exceptions import TierTuneCommandError, TierTuneCommandNotFound


class CommandT(NamedTuple):
    output: str
    error: str
    returncode: int


class Command:
    """
    **Implements command invocation**

    An instance of Command provides methods to invoke external
    commands in blocking mode. Control of stdout and stderr is
    given to the caller
    """

    @staticmethod
    def run(
        command: List[str],
        custom_env: Optional[MutableMapping[str, str]] = None,
        raise_on_error: bool = True,
        stderr_to_stdout: bool = False,
        raise_on_command_not_found: bool = True,
    ) -> Optional[CommandT]:
        """
        Execute a program and block the caller. The return value
        is a CommandT namedtuple containing the stdout, stderr
        and return code information. Unless raise_on_error is
        set to `False` an exception is thrown if the command
        exits with an error code not equal to zero. If
        raise_on_command_not_found is `False` and the command is
        not found, then `None` is returned.

        Example:

        .. code:: python

            result = Command.run(['ls', '-l'])

        :param list command: command and arguments
        :param dict custom_env: custom os.environ
        :param bool raise_on_error: control error behaviour
        :param bool stderr_to_stdout: redirects stderr to stdout
        :param bool raise_on_command_not_found: raise if command not found
        """
        environment = custom_env or os.environ
        cmd_abspath: Optional[str]
        if command[0].startswith("/"):
            cmd_abspath = command[0]
            if not os.path.exists(cmd_abspath):
                cmd_abspath = None
        else:
            cmd_abspath = Command.which(
                command[0], custom_env=environment, access_mode=os.X_OK
            )

        if not cmd_abspath:
            message = f'Command "{command[0]}" not found in the environment'
            if raise_on_command_not_found:
                raise TierTuneCommandNotFound(message)
            log.debug('EXEC: %s', message)
            return None
        stderr = subprocess.STDOUT if stderr_to_stdout else subprocess.PIPE
        log.debug('EXEC: [%s]', ' '.join(command))
        try:
            process = subprocess.Popen(
                [cmd_abspath] + command[1:],
                stdout=subprocess.PIPE,
                stderr=stderr,
                env=environment,
            )
        except (OSError, subprocess.SubprocessError) as e:
            raise TierTuneCommandError(
                f'{command[0]}: {type(e).__name__}: {format(e)}'
            ) from e

        output, error = process.communicate()
        if process.returncode != 0 and raise_on_error:
            if not error:
                error = bytes(b'(no output on stderr)')
            if not output:
                output = bytes(b'(no output on stdout)')
            log.debug(
                'EXEC: Failed with stderr: {0}, stdout: {1}'.format(
                    Codec.decode(error), Codec.decode(output)
                )
            )
            raise TierTuneCommandError(
                '{0}: stderr: {1}, stdout: {2}'.format(
                    command[0], Codec.decode(error), Codec.decode(output)
                )
            )
        return CommandT(
            output=Codec.decode(output),
            error=Codec.decode(error),
            returncode=process.returncode,
        )

    @staticmethod
    def which(
        filename: str,
        custom_env: Optional[MutableMapping[str, str]] = None,
        access_mode: int = os.F_OK | os.X_OK,
    ) -> Optional[str]:
        """
        Lookup file name in PATH

        :param string filename: file base name
        :param list alternative_lookup_paths: list of additional lookup paths
        :param list custom_env: a custom os.environ used to obtain ``$PATH``
        :param int access_mode:
            one of the os access modes or a combination of
            them (os.R_OK, os.W_OK and os.X_OK). If the provided access mode
            does not match the file is considered not existing
        :param str root_dir: the root path to look at
        """
        system_path = (
            custom_env.get("PATH") if custom_env else os.environ.get("PATH")
        ) or os.defpath
        lookup_paths = system_path.split(os.pathsep)
        log.debug(f'Looking for {filename} in {os.pathsep.join(lookup_paths)}')
        return shutil.which(
            filename, access_mode, path=os.pathsep.join(lookup_paths)
        )
