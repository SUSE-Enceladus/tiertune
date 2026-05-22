from unittest.mock import patch
from pytest import raises

from tiertune.gce import main
from tiertune.exceptions import TierTuneError


class TestGCE:
    @patch('tiertune.gce.SysCtl.apply')
    @patch('tiertune.gce.Config.read')
    @patch('tiertune.instance_type.InstanceType.new')
    def test_main(self, mock_InstanceType, mock_Config_read, mock_SysCtl_apply):
        main()
        mock_InstanceType.assert_called_once_with('gce')
        mock_SysCtl_apply.assert_called_once_with(
            mock_InstanceType.return_value, mock_Config_read.return_value
        )

    @patch('tiertune.gce.SysCtl.apply')
    @patch('sys.exit')
    def test_main_raises_known_error(self, mock_sys_exit, mock_SysCtl_apply):
        mock_SysCtl_apply.side_effect = TierTuneError('some')
        main()
        mock_sys_exit.assert_called_once_with(1)

    @patch('tiertune.gce.SysCtl.apply')
    def test_main_raises_unknown_error(self, mock_SysCtl_apply):
        mock_SysCtl_apply.side_effect = NotImplementedError
        with raises(NotImplementedError):
            main()
