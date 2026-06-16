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
import os

# optional system wide config file location
ETC_RUNTIME_CONFIG_FILE = {
    'azure': '/etc/tiertune-azure.yml',
    'gce': '/etc/tiertune-gce.yml',
    'aws': '/etc/tiertune-aws.yml',
}
ETC_RUNTIME_CONFIG_DIR = {
    'azure': '/etc/tiertune-azure.yml.d',
    'gce': '/etc/tiertune-gce.yml.d',
    'aws': '/etc/tiertune-aws.yml.d',
}

# distribution wide config file location, provided with the package
USR_RUNTIME_CONFIG_FILE = {
    'azure': '/usr/share/tiertune/tiertune-azure.yml',
    'gce': '/usr/share/tiertune/tiertune-gce.yml',
    'aws': '/usr/share/tiertune/tiertune-aws.yml',
}
USR_RUNTIME_CONFIG_DIR = {
    'azure': '/usr/share/tiertune/tiertune-azure.yml.d',
    'gce': '/usr/share/tiertune/tiertune-gce.yml.d',
    'aws': '/usr/share/tiertune/tiertune-aws.yml.d',
}

# systemd main settings overlay
SYSTEMD_CONF = '/etc/systemd/system.conf.d/tiertune.conf'
CPUPOWER_SERVICE = '/etc/systemd/system/cpupower.service'

# sysctl main settings overlay
SYSCTL_CONF = '/etc/sysctl.d/tiertune.conf'

# marker file to indicate settings have been applied
SETTINGS_APPLIED_FILE = '/var/cache/tiertune/settings_applied'


def write_state_file() -> None:
    os.makedirs(os.path.dirname(SETTINGS_APPLIED_FILE), exist_ok=True)
    with open(SETTINGS_APPLIED_FILE, 'w'):
        pass
