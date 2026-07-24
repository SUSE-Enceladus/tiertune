# Copyright (c) 2026 SUSE Software Solutions Germany GmbH.  All rights reserved.
#
# This file is part of tiertune.
#
# tiertune is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tiertune is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tiertune.  If not, see <http://www.gnu.org/licenses/>
#
import json
import re
import sys

from typing import Any, Optional
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TARGET = 'https://registry.suse.com/v2/_catalog'
SCOPE = 'registry:catalog:*'
AUTH_SCHEME = 'Bearer'


def get_auth_challenge(target: str) -> Optional[str]:
    request = Request(target, method='HEAD')
    try:
        with urlopen(request) as response:
            return response.headers.get('Www-Authenticate')
    except HTTPError as issue:
        return issue.headers.get('Www-Authenticate')


def extract_bearer_parameters(challenge: str) -> tuple[Optional[str], Optional[str]]:
    realm = re.search(r'realm="([^"]+)"', challenge, re.IGNORECASE)
    service = re.search(r'service="([^"]+)"', challenge, re.IGNORECASE)
    return (
        realm.group(1) if realm else None,
        service.group(1) if service else None,
    )


def fetch_text(target: str) -> str:
    with urlopen(target) as response:
        return response.read().decode()


def fetch_json(
    target: str,
    parameters: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    url = target
    if parameters:
        url = f'{target}?{urlencode(parameters)}'
    request = Request(url, headers=headers or {})
    with urlopen(request) as response:
        return json.load(response)


def main() -> int:
    challenge = get_auth_challenge(TARGET)
    if not challenge:
        print(
            'No authentication challenge found. '
            'The endpoint might be fully open or unreachable.'
        )
        sys.stdout.write(fetch_text(TARGET))
        return 0

    realm, service = extract_bearer_parameters(challenge)
    if not realm or not service:
        print('Failed to parse authentication challenge.')
        return 1

    print(f'REALM: {realm} SERVICE: {service} SCOPE: {SCOPE}')
    token_data = fetch_json(
        realm,
        parameters={'service': service, 'scope': SCOPE},
    )
    token = token_data.get('token') or token_data.get('access_token')
    if not token:
        print('Failed to acquire token.')
        return 1

    catalog = fetch_json(
        TARGET, headers={'Authorization': f'{AUTH_SCHEME} {token}'}
    )
    json.dump(catalog, sys.stdout, indent=4)
    sys.stdout.write('\n')
    return 0


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
