from unittest.mock import patch

from tiertune.instance_type.azure import InstanceTypeAzure


class TestInstanceTypeAzure:
    def setup_method(self):
        self.instance_type = InstanceTypeAzure()

    @patch('tiertune.command.Command.run')
    def test_get_instance_type(self, mock_Command_run):
        mock_Command_run.return_value.output = 'vmSize: Standard_DS1_v2'
        assert (
            self.instance_type.get_instance_type() == 'vmSize: Standard_DS1_v2'
        )
        mock_Command_run.assert_called_once_with(['azuremetadata', '--vmSize'])
