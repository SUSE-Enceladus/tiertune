from unittest.mock import patch
from pytest import raises

from tiertune.exceptions import TierTuneInstanceTypeError
from tiertune.instance_type import InstanceType


class TestInstanceType:
    def test_instance_type_not_implemented(self):
        with raises(TierTuneInstanceTypeError):
            InstanceType.new('bogus')

    @patch('tiertune.instance_type.aws.InstanceTypeAws')
    def test_instance_type_aws(self, mock_instance_type):
        InstanceType.new('aws')
        mock_instance_type.assert_called_once_with()

    @patch('tiertune.instance_type.gce.InstanceTypeGce')
    def test_instance_type_gce(self, mock_instance_type):
        InstanceType.new('gce')
        mock_instance_type.assert_called_once_with()

    @patch('tiertune.instance_type.azure.InstanceTypeAzure')
    def test_instance_type_azure(self, mock_instance_type):
        InstanceType.new('azure')
        mock_instance_type.assert_called_once_with()
