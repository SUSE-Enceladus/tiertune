from unittest.mock import patch, Mock

from tiertune.sysctl import SysCtl
from tiertune.instance_type import InstanceType
from tiertune.config import Config
import tiertune.defaults as defaults


class TestSysCtl:
    @patch('tiertune.command.Command.run')
    def test_set(self, mock_Command_run):
        SysCtl.set('net.ipv4.ip_local_port_range="9000 65499"')
        mock_Command_run.assert_called_once_with(
            ['sysctl', '-w', 'net.ipv4.ip_local_port_range="9000 65499"']
        )

    @patch('tiertune.command.Command.run')
    def test_apply(self, mock_Command_run):
        defaults.ETC_RUNTIME_CONFIG_FILE = {'aws': '../data/tiertune-aws.yml'}
        instance = InstanceType.new('aws')
        instance.get_instance_type = Mock(
            return_value='an_aws_instance_type_name'
        )
        SysCtl.apply(instance, Config.read_aws())
        mock_Command_run.assert_called_once_with(
            ['sysctl', '-w', 'net.core.rmem_max=83886080']
        )
