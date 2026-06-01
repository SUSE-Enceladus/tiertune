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
import os
import logging as log
from typing import Dict
import yaml

import tiertune.defaults as defaults


class Config:
    """
    **Implements config file interface**
    """

    @staticmethod
    def _merge(dict_master, dict_slave):
        """
        Simple deep merge adding everything from a slave dict to a master
        """
        for key, value in dict_master.items():
            if key in dict_slave:
                dict_slave[key] = Config._merge(value, dict_slave[key])
        dict_master.update(dict_slave)
        return dict_master

    @staticmethod
    def read(csp_name: str) -> Dict[str, Dict[str, Dict[str, str]]]:
        runtime_config: Dict[str, Dict[str, Dict[str, str]]] = {}
        config_file = defaults.ETC_RUNTIME_CONFIG_FILE.get(csp_name, '')
        if not os.path.exists(config_file):
            config_file = defaults.USR_RUNTIME_CONFIG_FILE.get(csp_name, '')
        if os.path.exists(config_file):
            log.info(f'Reading runtime config file: {config_file!r}')
            with open(config_file, 'r') as config:
                runtime_config = yaml.safe_load(config) or {}

            if config_file == defaults.ETC_RUNTIME_CONFIG_FILE.get(
                csp_name, ''
            ):
                config_dir = defaults.ETC_RUNTIME_CONFIG_DIR.get(csp_name)
            elif config_file == defaults.USR_RUNTIME_CONFIG_FILE.get(
                csp_name, ''
            ):
                config_dir = defaults.USR_RUNTIME_CONFIG_DIR.get(csp_name, '')

            if config_dir and os.path.isdir(config_dir):
                for config_file in sorted(os.listdir(config_dir)):
                    if config_file.endswith('.yml'):
                        config_file_path = os.path.normpath(
                            os.sep.join([config_dir, config_file])
                        )
                        log.info(
                            f'--> Reading addon runtime config file: {config_file_path!r}'
                        )
                        with open(config_file_path, 'r') as config:
                            additional_config = yaml.safe_load(config) or {}
                            runtime_config = Config._merge(
                                runtime_config, additional_config
                            )
        return runtime_config

    @staticmethod
    def read_azure() -> Dict[str, Dict[str, Dict[str, str]]]:
        return Config.read('azure')

    @staticmethod
    def read_gce() -> Dict[str, Dict[str, Dict[str, str]]]:
        return Config.read('gce')

    @staticmethod
    def read_aws() -> Dict[str, Dict[str, Dict[str, str]]]:
        return Config.read('aws')
