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
from string import Template

from tiertune.command import Command
from tiertune.defaults import KERNELWORKQUEUE_SERVICE
from tiertune.defaults import write_state_file
from tiertune.instance_type.base import InstanceTypeBase


class KernelWorkQueue:
    """
    **Implements kernel workqueue settings interface**
    """

    _template_file = os.path.join(
        os.path.dirname(__file__), 'template', 'kernelworkqueue.service'
    )

    def __init__(self) -> None:
        self._set_called = False

    def __enter__(self) -> 'KernelWorkQueue':
        self._set_called = False
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        if exc_type is None and self._set_called:
            write_state_file()

    def set(self, key: str, value: str) -> None:
        """
        Set a kernel workqueue setting by key-value pair.
        """
        self._set_called = True
        if key == 'watchdog_threshold' and value:
            if not value.isdigit():
                log.warning(
                    f'Invalid value for {key}: {value!r} (expected a non-negative integer)'
                )
                return
            log.info(f'Set KernelWorkQueue setting: {key}={value}')
            command = [
                'bash',
                '-c',
                f'echo {value} > /sys/module/workqueue/parameters/watchdog_thresh',
            ]
            Command.run(command)
            self._write_service(command)
        else:
            log.info(
                'Unknown KernelWorkQueue setting: {} with value {}'.format(
                    key, value or ''
                )
            )

    def _write_service(self, command: list[str]) -> None:
        """
        Generate and write a systemd service file from the template
        using the provided command as the ExecStart value.
        """
        with open(self._template_file, 'r') as template:
            kernelworkqueue_service_source = Template(template.read())
            service = kernelworkqueue_service_source.substitute(
                {'command': ' '.join(command)}
            )
        os.makedirs(os.path.dirname(KERNELWORKQUEUE_SERVICE), exist_ok=True)
        with open(KERNELWORKQUEUE_SERVICE, 'w') as service_file:
            service_file.write(service)

    @staticmethod
    def apply(
        instance: InstanceTypeBase, config: Dict[str, Dict[str, Dict[str, str]]]
    ) -> None:
        instance_type = instance.get_instance_type()
        if instance_type:
            with KernelWorkQueue() as kernelworkqueue:
                settings_dict = instance.get_settings(
                    instance_type, config
                ).get('kernelworkqueue', {})
                for key in sorted(settings_dict.keys()):
                    kernelworkqueue.set(key, settings_dict.get(key, ''))
