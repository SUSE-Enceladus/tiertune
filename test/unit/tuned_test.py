from unittest.mock import patch, Mock

from tiertune.tuned import TuneD
from tiertune.instance_type import InstanceType
from tiertune.config import Config
import tiertune.defaults as defaults


class TestTuneD:
    @patch('tiertune.command.Command.run')
    def test_set(self, mock_Command_run):
        TuneD.set('some_profile')
        mock_Command_run.assert_called_once_with(
            ['tuned-adm', 'profile', 'some_profile']
        )

    @patch('tiertune.tuned.TuneD.set')
    def test_apply(self, mock_TuneD_set):
        defaults.ETC_RUNTIME_CONFIG_FILE = {'aws': '../data/tiertune-aws.yml'}
        instance = InstanceType.new('aws')
        instance.get_instance_type = Mock(
            return_value='an_aws_instance_type_name'
        )
        TuneD.apply(instance, Config.read_aws())
        mock_TuneD_set.assert_called_once_with('some')
