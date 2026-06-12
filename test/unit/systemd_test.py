import io
from unittest.mock import patch, Mock, MagicMock

from tiertune.systemd import SystemD
from tiertune.instance_type import InstanceType
from tiertune.config import Config
import tiertune.defaults as defaults


class TestSystemD:
    def test_set(self):
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=io.IOBase)
            file_handle = mock_open.return_value.__enter__.return_value
            SystemD().set('DefaultTimeoutStartSec=300s')
            mock_open.assert_called_once_with(
                '/etc/systemd/system.conf.d/tiertune.conf', 'a'
            )
            file_handle.write.assert_called_once_with(
                'DefaultTimeoutStartSec=300s\n'
            )

    @patch('tiertune.systemd.SystemD.set')
    @patch('tiertune.command.Command.run')
    @patch('os.path.exists')
    @patch('os.unlink')
    def test_apply(
        self,
        mock_os_unlink,
        mock_os_path_exists,
        mock_Command_run,
        mock_SystemD_set,
    ):
        mock_os_path_exists.return_value = True
        defaults.ETC_RUNTIME_CONFIG_FILE = {'aws': '../data/tiertune-aws.yml'}
        instance = InstanceType.new('aws')
        instance.get_instance_type = Mock(
            return_value='an_aws_instance_type_name'
        )
        SystemD.apply(instance, Config.read_aws())
        mock_os_unlink.assert_called_once_with(
            '/etc/systemd/system.conf.d/tiertune.conf'
        )
        mock_Command_run.assert_called_once_with(['systemctl', 'daemon-reload'])

    @patch('tiertune.systemd.write_state_file')
    def test_context_manager_writes_state_file(self, mock_write_state_file):
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=io.IOBase)
            with SystemD() as systemd:
                systemd.set('DefaultTimeoutStartSec=300s')
        mock_write_state_file.assert_called_once()

    @patch('tiertune.systemd.write_state_file')
    def test_context_manager_without_set_does_not_write_state_file(
        self, mock_write_state_file
    ):
        with SystemD():
            pass
        assert not mock_write_state_file.called
