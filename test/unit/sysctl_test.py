from unittest.mock import patch

from tiertune.sysctl import SysCtl


class TestSysCtl:
    @patch('tiertune.command.Command.run')
    def test_set(self, mock_Command_run):
        SysCtl.set('net.ipv4.ip_local_port_range="9000 65499"')
        mock_Command_run.assert_called_once_with(
            ['sysctl', '-w', 'net.ipv4.ip_local_port_range="9000 65499"']
        )
