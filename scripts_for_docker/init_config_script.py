#!/usr/bin/env python

import json
from getpass import getpass


def get_database_server() -> str:
    server: str = input('Database server address: ').strip()
    if len(server) > 3:
        return server
    print('Incorrect database server address.\n')
    return get_database_server()


def get_database_name() -> str:
    db_name: str = input('Database name: ').strip()
    return db_name


def get_database_user() -> str:
    db_username: str = input('Database username: ').strip()
    return db_username


def get_database_password() -> str:
    password: str = getpass('Database user password: ').strip()
    return password


def get_api_keys(api_keys: list = None) -> list[str]:
    if api_keys is None:
        api_keys = []
    if len(api_keys) > 0:
        prompt: str = 'You can add an additional key (if you want to finish entering the keys - enter "N"): '
    else:
        prompt: str = \
            'Enter your API key "ilovepdf.com" for conversion to pdf (if you want to skip this step - enter "N"): '
    key: str = input(prompt).strip()
    if key.upper() == 'N':
        return api_keys
    api_keys.append(key)
    return get_api_keys(api_keys)


if __name__ == '__main__':
    with open('/usr/src/app/config.json', 'r') as config_file:
        config: dict = json.load(config_file)
    config['db']['server'] = get_database_server()
    config['db']['database'] = get_database_name()
    config['db']['user'] = get_database_user()
    config['db']['password'] = get_database_password()
    config['convertor']['public_keys'] = get_api_keys()
    with open('/usr/src/app/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

