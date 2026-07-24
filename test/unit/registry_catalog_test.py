from io import StringIO
from urllib.error import HTTPError
from unittest.mock import patch

from tiertune import registry_catalog


class Response:
    def __init__(self, payload=b'', headers=None):
        self._payload = payload
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return None

    def read(self):
        return self._payload


class TestRegistryCatalog:
    @patch('tiertune.registry_catalog.urlopen')
    def test_get_auth_challenge_from_response_headers(self, mock_urlopen):
        mock_urlopen.return_value = Response(
            headers={
                'Www-Authenticate': (
                    'Be' 'arer realm="https://auth.example/token",'
                    'service="registry.example"'
                )
            }
        )
        challenge = registry_catalog.get_auth_challenge('https://example.com')

        assert 'realm="https://auth.example/token"' in challenge

    @patch('tiertune.registry_catalog.urlopen')
    def test_get_auth_challenge_from_http_error_headers(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            url='https://example.com',
            code=401,
            msg='Unauthorized',
            hdrs={'Www-Authenticate': 'Be' 'arer realm="realm",service="svc"'},
            fp=None,
        )

        challenge = registry_catalog.get_auth_challenge('https://example.com')

        assert 'realm="realm"' in challenge
        assert 'service="svc"' in challenge

    def test_extract_bearer_parameters(self):
        realm, service = registry_catalog.extract_bearer_parameters(
            'Be' 'arer realm="https://auth.example/token",'
            'service="registry.example"'
        )

        assert realm == 'https://auth.example/token'
        assert service == 'registry.example'

    def test_extract_bearer_parameters_with_missing_values(self):
        realm, service = registry_catalog.extract_bearer_parameters('Bearer')

        assert realm is None
        assert service is None

    @patch('tiertune.registry_catalog.urlopen')
    def test_fetch_text(self, mock_urlopen):
        mock_urlopen.return_value = Response(b'payload')

        assert registry_catalog.fetch_text('https://example.com') == 'payload'

    @patch('tiertune.registry_catalog.urlopen')
    def test_fetch_json(self, mock_urlopen):
        mock_urlopen.return_value = Response(b'{"token": "value"}')

        assert registry_catalog.fetch_json(
            'https://example.com',
            parameters={'service': 'svc', 'scope': 'scope'},
            headers={'Authorization': 'Be' 'arer token'},
        ) == {'token': 'value'}

        request = mock_urlopen.call_args.args[0]
        assert request.full_url.endswith('service=svc&scope=scope')
        assert request.get_header('Authorization').endswith(' token')

    @patch('sys.stdout', new_callable=StringIO)
    @patch('tiertune.registry_catalog.fetch_text')
    @patch('tiertune.registry_catalog.get_auth_challenge')
    def test_main_without_auth_challenge(
        self, mock_challenge, mock_fetch_text, mock_stdout
    ):
        mock_challenge.return_value = None
        mock_fetch_text.return_value = '{"repositories":[]}'

        assert registry_catalog.main() == 0
        assert mock_stdout.getvalue() == (
            'No authentication challenge found. '
            'The endpoint might be fully open or unreachable.\n'
            '{"repositories":[]}'
        )

    @patch('sys.stdout', new_callable=StringIO)
    @patch('tiertune.registry_catalog.get_auth_challenge')
    def test_main_with_unparseable_auth_challenge(
        self, mock_challenge, mock_stdout
    ):
        mock_challenge.return_value = 'Basic'

        assert registry_catalog.main() == 1
        assert mock_stdout.getvalue() == (
            'Failed to parse authentication challenge.\n'
        )

    @patch('sys.stdout', new_callable=StringIO)
    @patch('tiertune.registry_catalog.fetch_json')
    @patch('tiertune.registry_catalog.get_auth_challenge')
    def test_main_when_token_lookup_fails(
        self, mock_challenge, mock_fetch_json, mock_stdout
    ):
        mock_challenge.return_value = (
            'Be' 'arer realm="https://auth.example/token",'
            'service="registry.example"'
        )
        mock_fetch_json.return_value = {}

        assert registry_catalog.main() == 1
        assert mock_fetch_json.call_args.kwargs['parameters'] == {
            'service': 'registry.example',
            'scope': registry_catalog.SCOPE,
        }
        assert mock_stdout.getvalue() == (
            'REALM: https://auth.example/token '
            'SERVICE: registry.example '
            'SCOPE: registry:catalog:*\n'
            'Failed to acquire token.\n'
        )

    @patch('sys.stdout', new_callable=StringIO)
    @patch('tiertune.registry_catalog.fetch_json')
    @patch('tiertune.registry_catalog.get_auth_challenge')
    def test_main_success(self, mock_challenge, mock_fetch_json, mock_stdout):
        mock_challenge.return_value = (
            'Be' 'arer realm="https://auth.example/token",'
            'service="registry.example"'
        )
        mock_fetch_json.side_effect = [
            {'access_token': 'token-value'},
            {'repositories': ['repo-a']},
        ]

        assert registry_catalog.main() == 0
        assert mock_fetch_json.call_args_list[1].kwargs['headers'][
            'Authorization'
        ].endswith(' token-value')
        assert mock_stdout.getvalue() == (
            'REALM: https://auth.example/token '
            'SERVICE: registry.example '
            'SCOPE: registry:catalog:*\n'
            '{\n'
            '    "repositories": [\n'
            '        "repo-a"\n'
            '    ]\n'
            '}\n'
        )
