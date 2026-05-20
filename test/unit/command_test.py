from unittest.mock import patch
from collections import namedtuple
from pytest import raises
import unittest.mock as mock
import os

import pytest

from tiertune.command import Command

from tiertune.exceptions import TierTuneCommandError, TierTuneCommandNotFound


class TestCommand:
    @patch('tiertune.command.Command.which')
    @patch('subprocess.Popen')
    def test_run_raises_error(self, mock_popen, mock_which):
        mock_which.return_value = 'command'
        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(
            return_value=[str.encode(''), str.encode('')]
        )
        mock_process.returncode = 1
        mock_popen.return_value = mock_process
        with raises(TierTuneCommandError):
            Command.run(['command', 'args'])

    @patch('tiertune.command.Command.which')
    @patch('subprocess.Popen')
    def test_run_failure(self, mock_popen, mock_which):
        mock_which.return_value = 'command'
        mock_popen.side_effect = OSError('Run failure')
        with raises(TierTuneCommandError):
            Command.run(['command', 'args'])

    def test_run_invalid_environment(self):
        with raises(TierTuneCommandNotFound):
            Command.run(['command', 'args'], custom_env={'PATH': '/root'})

    @patch('tiertune.command.Command.which')
    @patch('subprocess.Popen')
    def test_run_does_not_raise_error(self, mock_popen, mock_which):
        mock_which.return_value = 'command'
        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(
            return_value=[str.encode('stdout'), str.encode('')]
        )
        mock_process.returncode = 1
        mock_popen.return_value = mock_process
        result = Command.run(['command', 'args'], os.environ, False)
        assert result.error == ''
        assert result.output == 'stdout'

    @patch('tiertune.command.Command.which')
    def test_run_does_not_raise_error_if_command_not_found(self, mock_which):
        mock_which.return_value = None
        result = Command.run(
            ['command', 'args'], os.environ, raise_on_command_not_found=False
        )
        assert result is None

    @patch('tiertune.command.Command.which')
    @patch('os.path.exists')
    @patch('subprocess.Popen')
    def test_run_does_not_call_which_for_abspaths(
        self, mock_popen, mock_exists, mock_which
    ):
        mock_exists.return_value = True
        proc = mock.MagicMock()
        proc.communicate.return_value = (
            str.encode("stdout"),
            str.encode("stderr"),
        )
        proc.returncode = 0
        mock_popen.return_value = proc

        result = Command.run(['/bin/command', 'args'])
        mock_which.assert_not_called()
        assert result is not None

    @patch('tiertune.command.Command.which')
    @patch('os.path.exists')
    def test_run_fails_for_non_existent_abspath(self, mock_exists, mock_which):
        mock_exists.return_value = False

        with pytest.raises(TierTuneCommandNotFound) as cmd_not_found_err:
            Command.run(['/bin/command', 'args'])

        mock_which.assert_not_called()
        assert '"/bin/command" not found' in str(cmd_not_found_err.value)

    @patch('os.access')
    @patch('os.path.exists')
    @patch('subprocess.Popen')
    def test_run(self, mock_popen, mock_exists, mock_access):
        mock_exists.return_value = True
        command_run = namedtuple('command', ['output', 'error', 'returncode'])
        run_result = command_run(output='stdout', error='stderr', returncode=0)
        mock_process = mock.Mock()
        mock_process.communicate = mock.Mock(
            return_value=[str.encode('stdout'), str.encode('stderr')]
        )
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        mock_access.return_value = True
        assert Command.run(['command', 'args']) == run_result

    def test_run_command_does_not_exist(self):
        with raises(TierTuneCommandNotFound):
            Command.run(['does-not-exist'])
