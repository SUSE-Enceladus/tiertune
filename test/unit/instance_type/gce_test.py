from unittest.mock import patch

from tiertune.instance_type.gce import InstanceTypeGce


class TestInstanceTypeGce:
    def setup_method(self):
        self.instance_type = InstanceTypeGce()

    @patch('tiertune.command.Command.run')
    def test_get_instance_type(self, mock_Command_run):
        mock_Command_run.return_value.output = (
            'projects/284177885636/machineTypes/n1-standard-1'
        )
        assert (
            self.instance_type.get_instance_type()
            == 'projects/284177885636/machineTypes/n1-standard-1'
        )
        mock_Command_run.assert_called_once_with(
            ['gcemetadata', '--query', 'instance', '--machine-type']
        )
