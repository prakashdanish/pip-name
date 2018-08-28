"""Check whether a package name is available on PyPi"""

import argparse
import requests

BASE_URL = 'https://pypi.org/pypi'
RED = '\033[31m'
BOLD = '\033[1m'
GREEN = '\033[32m'
RESET = '\033[0m'
LENGTH = 'Package name seems way too long, try shortening it'
UPPERCASE = 'Use of uppercase letters are discouraged'
SEPERATOR = 'If you must use a separator, consider using `-`'


def get_response(name):
    """Request response from PyPi API"""
    target_url = '{0}/{1}/json'.format(BASE_URL, name)
    response = requests.get(target_url)

    if response.status_code == 404:
        response = None
    else:
        response = response.json()

    return response


def inspect_name(name):
    """Checks name against PEP8's naming conventions"""
    suggestions = list()

    if len(name) > 12:
        suggestions.append(LENGTH)
    if '-' in name or ' ' in name:
        suggestions.append(SEPERATOR)
    if any(x.isupper() for x in name):
        suggestions.append(UPPERCASE)

    return '\n'.join(suggestions)


def is_name_taken(name):
    """Check module filename for conflict"""
    response = get_response(name)

    if response:
        module_name = response.get('info').get('package_url').split('/')[-2]
        return True if name.lower() == module_name.lower() else False

    return False


def main():
    """Handle arguments and flow"""
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='name of package you want to check', type=str)
    args = parser.parse_args()

    if is_name_taken(args.name):
        print('{0}{1}{2} is unavailable.'.format(RED, args.name, RESET))
    else:
        print('{0}{1}{2}  is available\n\nSuggestions:\n{3}'.format(
            GREEN, args.name, RESET, inspect_name(args.name)))
