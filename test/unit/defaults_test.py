from unittest.mock import patch

from tiertune.defaults import SETTINGS_APPLIED_FILE
from tiertune.defaults import write_state_file


class TestDefaults:
    @patch('builtins.open')
    def test_write_state_file(self, mock_open):
        write_state_file()
        mock_open.assert_called_once_with(SETTINGS_APPLIED_FILE, 'w')
