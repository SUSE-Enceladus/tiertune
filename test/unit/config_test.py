from tiertune.config import Config


class TestConfig:
    def test_read(self):
        assert Config.read('../data/tiertune-aws.yml') == {
            'an_aws_instance_type_name': {
                'sysctl': ['net.core.rmem_max=83886080']
            }
        }
        assert Config.read('bogus') == {}
