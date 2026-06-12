from unittest.mock import patch, Mock

from tiertune.cpupower import CPUPower
from tiertune.instance_type import InstanceType
from tiertune.config import Config
import tiertune.defaults as defaults


class TestCPUPower:
    @patch('tiertune.command.Command.run')
    def test_set(self, mock_Command_run):
        CPUPower.set('force_latency', '6')
        mock_Command_run.assert_called_once_with(
            ['cpupower', 'idle-set', '--disable-by-latency', '6']
        )

    @patch('tiertune.command.Command.run')
    def test_set_unknown_setting(self, mock_Command_run):
        CPUPower.set('some', 'some')
        assert not mock_Command_run.called

    @patch('tiertune.cpupower.CPUPower.set')
    def test_apply(self, mock_CPUPower_set):
        defaults.ETC_RUNTIME_CONFIG_FILE = {'aws': '../data/tiertune-aws.yml'}
        instance = InstanceType.new('aws')
        instance.get_instance_type = Mock(
            return_value='an_aws_instance_type_name'
        )
        CPUPower.apply(instance, Config.read_aws())
        mock_CPUPower_set.assert_called_once_with('force_latency', '6')

    @patch('tiertune.cpupower.write_state_file')
    @patch('tiertune.command.Command.run')
    def test_context_manager_writes_state_file(
        self, mock_Command_run, mock_write_state_file
    ):
        with CPUPower() as cpupower:
            cpupower.set('force_latency', '6')
        mock_Command_run.assert_called_once_with(
            ['cpupower', 'idle-set', '--disable-by-latency', '6']
        )
        mock_write_state_file.assert_called_once()

    @patch('tiertune.cpupower.write_state_file')
    def test_context_manager_without_set_does_not_write_state_file(
        self, mock_write_state_file
    ):
        with CPUPower():
            pass
        assert not mock_write_state_file.called
