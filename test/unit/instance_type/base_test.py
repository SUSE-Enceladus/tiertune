from pytest import raises

from tiertune.instance_type.base import InstanceTypeBase


class TestInstanceTypeBase:
    def test_get_instance_type(self):
        instance_type = InstanceTypeBase()
        with raises(NotImplementedError):
            instance_type.get_instance_type()

    def test_get_settings(self):
        config = {
            '^.*/n1-standard-1$': {'sysctl': ['net.core.rmem_max=83886080']}
        }
        instance_type = InstanceTypeBase()
        assert instance_type.get_settings(
            'projects/123456789/machineTypes/n1-standard-1', config
        ) == {'sysctl': ['net.core.rmem_max=83886080']}
