from unittest.mock import patch

from tiertune.config import Config
import tiertune.defaults as defaults


class TestConfig:
    def test_read(self):
        defaults.ETC_RUNTIME_CONFIG_FILE = {'aws': '../data/tiertune-aws.yml'}
        assert Config.read('aws') == {
            'an_aws_instance_type_name': {
                'sysctl': {'net.core.rmem_max': '83886080'},
                'systemd': {'DefaultTimeoutStartSec': '300s'},
            }
        }
        assert Config.read('bogus') == {}

    def test_read_addon_etc(self):
        defaults.ETC_RUNTIME_CONFIG_FILE = {'aws': '../data/tiertune-aws.yml'}
        defaults.ETC_RUNTIME_CONFIG_DIR = {'aws': '../data/tiertune-aws.yml.d'}
        assert Config.read('aws') == {
            'an_aws_instance_type_name': {
                'sysctl': {'net.core.rmem_max': '83886080', 'some': 'some'},
                'systemd': {'DefaultTimeoutStartSec': '300s'},
            }
        }

    def test_read_addon_usr(self):
        defaults.USR_RUNTIME_CONFIG_FILE = {'aws': '../data/tiertune-aws.yml'}
        defaults.USR_RUNTIME_CONFIG_DIR = {'aws': '../data/tiertune-aws.yml.d'}
        assert Config.read('aws') == {
            'an_aws_instance_type_name': {
                'sysctl': {'net.core.rmem_max': '83886080', 'some': 'some'},
                'systemd': {'DefaultTimeoutStartSec': '300s'},
            }
        }

    @patch('tiertune.config.Config.read')
    def test_read_azure(self, mock_Config_read):
        Config.read_azure()
        mock_Config_read.assert_called_once_with('azure')

    @patch('tiertune.config.Config.read')
    def test_read_gce(self, mock_Config_read):
        Config.read_gce()
        mock_Config_read.assert_called_once_with('gce')

    @patch('tiertune.config.Config.read')
    def test_read_aws(self, mock_Config_read):
        Config.read_aws()
        mock_Config_read.assert_called_once_with('aws')
