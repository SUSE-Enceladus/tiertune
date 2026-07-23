from unittest.mock import MagicMock, Mock, patch, call

from tiertune.kernelworkqueue import KernelWorkQueue
from tiertune.instance_type import InstanceType
from tiertune.config import Config
import tiertune.defaults as defaults


class TestKernelWorkQueue:
    @patch('tiertune.command.Command.run')
    @patch('os.makedirs')
    def test_set(self, mock_os_makedirs, mock_Command_run):
        with patch('builtins.open', create=True) as mock_open:
            template_handle = MagicMock()
            template_handle.read.return_value = (
                '[Service]\nExecStart=$command\n'
            )
            service_handle = MagicMock()
            mock_open.side_effect = [
                MagicMock(__enter__=MagicMock(return_value=template_handle)),
                MagicMock(__enter__=MagicMock(return_value=service_handle)),
            ]
            KernelWorkQueue().set('watchdog_threshold', '30')

        assert mock_Command_run.call_args_list == [
            call(
                [
                    'bash',
                    '-c',
                    'echo 30 > /sys/module/workqueue/parameters/watchdog_thresh',
                ]
            ),
        ]
        mock_os_makedirs.assert_called_once_with(
            '/etc/systemd/system', exist_ok=True
        )
        service_handle.write.assert_called_once_with(
            '[Service]\nExecStart=bash -c echo 30 > /sys/module/workqueue/parameters/watchdog_thresh\n'
        )

    @patch('tiertune.command.Command.run')
    def test_set_unknown_setting(self, mock_Command_run):
        KernelWorkQueue().set('some', 'some')
        assert not mock_Command_run.called

    @patch('tiertune.command.Command.run')
    def test_set_invalid_value(self, mock_Command_run):
        KernelWorkQueue().set('watchdog_threshold', 'not_a_number')
        assert not mock_Command_run.called

    @patch('tiertune.kernelworkqueue.KernelWorkQueue.set')
    def test_apply(self, mock_KernelWorkQueue_set):
        defaults.ETC_RUNTIME_CONFIG_FILE = {'aws': '../data/tiertune-aws.yml'}
        instance = InstanceType.new('aws')
        instance.get_instance_type = Mock(
            return_value='an_aws_instance_type_name'
        )
        KernelWorkQueue.apply(instance, Config.read_aws())
        mock_KernelWorkQueue_set.assert_called_once_with(
            'watchdog_threshold', '120'
        )

    @patch('tiertune.kernelworkqueue.write_state_file')
    @patch('tiertune.kernelworkqueue.KernelWorkQueue._write_service')
    @patch('tiertune.command.Command.run')
    def test_context_manager_writes_state_file(
        self, mock_Command_run, mock_write_service, mock_write_state_file
    ):
        with KernelWorkQueue() as kernelworkqueue:
            kernelworkqueue.set('watchdog_threshold', '30')
        mock_write_service.assert_called_once_with(
            [
                'bash',
                '-c',
                'echo 30 > /sys/module/workqueue/parameters/watchdog_thresh',
            ]
        )
        mock_write_state_file.assert_called_once()

    @patch('tiertune.kernelworkqueue.write_state_file')
    def test_context_manager_without_set_does_not_write_state_file(
        self, mock_write_state_file
    ):
        with KernelWorkQueue():
            pass
        assert not mock_write_state_file.called
