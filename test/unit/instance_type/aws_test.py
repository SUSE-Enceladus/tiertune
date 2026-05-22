from unittest.mock import patch

from tiertune.instance_type.aws import InstanceTypeAws


class TestInstanceTypeAws:
    def setup_method(self):
        self.instance_type = InstanceTypeAws()

    @patch('tiertune.command.Command.run')
    def test_get_instance_type(self, mock_Command_run):
        mock_Command_run.return_value.output = 't3.micro'
        assert self.instance_type.get_instance_type() == 't3.micro'
        mock_Command_run.assert_called_once_with(
            ['ec2metadata', '--instance-type']
        )
