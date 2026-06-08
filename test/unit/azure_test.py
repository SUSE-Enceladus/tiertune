from unittest.mock import patch
from pytest import raises

from tiertune.azure import main
from tiertune.exceptions import TierTuneError


class TestAzure:
    @patch('tiertune.azure.TuneD.apply')
    @patch('tiertune.azure.CPUPower.apply')
    @patch('tiertune.azure.SystemD.apply')
    @patch('tiertune.azure.SysCtl.apply')
    @patch('tiertune.azure.Config.read')
    @patch('tiertune.instance_type.InstanceType.new')
    def test_main(
        self,
        mock_InstanceType,
        mock_Config_read,
        mock_SysCtl_apply,
        mock_SystemD_apply,
        mock_CPUPower_apply,
        mock_TuneD_apply,
    ):
        main()
        mock_InstanceType.assert_called_once_with('azure')
        mock_SysCtl_apply.assert_called_once_with(
            mock_InstanceType.return_value, mock_Config_read.return_value
        )
        mock_SystemD_apply.assert_called_once_with(
            mock_InstanceType.return_value, mock_Config_read.return_value
        )
        mock_CPUPower_apply.assert_called_once_with(
            mock_InstanceType.return_value, mock_Config_read.return_value
        )
        mock_TuneD_apply.assert_called_once_with(
            mock_InstanceType.return_value, mock_Config_read.return_value
        )

    @patch('tiertune.azure.SysCtl.apply')
    @patch('sys.exit')
    def test_main_raises_known_error(self, mock_sys_exit, mock_SysCtl_apply):
        mock_SysCtl_apply.side_effect = TierTuneError('some')
        main()
        mock_sys_exit.assert_called_once_with(1)

    @patch('tiertune.azure.SysCtl.apply')
    def test_main_raises_unknown_error(self, mock_SysCtl_apply):
        mock_SysCtl_apply.side_effect = NotImplementedError
        with raises(NotImplementedError):
            main()
