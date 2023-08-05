#!/usr/bin/env python
# -*- coding: utf8 -*-

""" Pole Vault package
"""

import os
import sys
import json

from getpass import getpass

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from collections import OrderedDict

import click

from .encryption import encrypt_credentials, decrypt_credentials
from .config import merge_default, get_file_type_and_mtime, get_config, write_yaml

import yaml


class Client(object):
    """ Client class that mimics the behavior of the Client class
        of the hvac package, which is used to access credentials
        stored in Hashicorp's Vault.
    """

    def __init__(self, key=None):
        """ Client constructor

            Parameters
            ----------
            key : str, optional

                The key to be used to decrypt the crendentials, in case they
                are encrypted.
        """
        self.key = key

    def read(self, *args):
        path = '/'.join(args)
        tokens = path.split('/')
        entry = tokens[-1]
        path = '/'.join(tokens[:-1])
        path, file_type, file_mtime = get_file_type_and_mtime(path)
        data = get_config(path, file_type, default=False)
        if self.key:
            data = decrypt_credentials(data, self.key)
        data = merge_default(data)
        result = data[entry]
        if type(result) is OrderedDict:
            result = dict(result)
        return { 'data': result }


CONTEXT_SETTINGS = {
    "help_option_names": ['-h', '--help'],
}

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    # '''
    # Encrypts and decrypts credentials, stores them
    # in a .ini, .conf, .json, .yml, or .yaml file,
    # and migrates them to and from Hashicorp's vault.
    # '''
    pass


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('path')
@click.option('-k', '--key', default='', help="AES GCM 256 encryption key in base64 enconding.")
@click.option('-d', '--default', is_flag=True, help="Merge the DEFAULT entry with the other entries.")
@click.option('-o', '--output', default='', help="File type for the encrypted file that is saved.")
def encrypt(path, key, default, output):
    """ Encrypts credentials
        in a .ini, .conf, .json, .yml, or .yaml file type.

        The PATH argument is the path to the file that contains the credentials.
        Its file type can be ommited.

        The KEY argument is the encryption key in base64 encoding.
        If ommited then one is generated and presented to the user.
    """
    if not key:
        key = getpass('Encryption key: ')

    path, file_type, file_mtime = get_file_type_and_mtime(path)
    config = get_config(path, file_type, default)
    data = encrypt_credentials(config, key)

    if output:
        if output[0] == '.':
            output = output[1:]
        file_type = '.' + output.lower()

    with open(path + file_type, 'w') as save_file:
        if file_type == '.json':
            json.dump(data, save_file, indent=2)

        elif file_type in {'.ini', '.conf'}:
            if default:
                default_section = 'DEFAULT'
            else:
                default_section = 'DEFAULT' + os.urandom(16).hex()

            for heading in data:
                save_file.write("[{}]\n".format(heading))
                for item in data[heading]:
                    save_file.write("{} = {}\n".format(item, data[heading][item]))
                save_file.write("\n")

        else:
            write_yaml(save_file, data)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('path')
@click.option('-k', '--key', default='', help="AES GCM 256 encryption key in base64 enconding.")
@click.option('-d', '--default', is_flag=True, help="Merge the DEFAULT entry with the other entries.")
@click.option('-o', '--output', default='', help="File type for the encrypted file that is saved.")
@click.option('-u', '--url', default='', help="Hashicorp's Vault URL.")
@click.option('-t', '--token', default='', help="Hashicorp's Vault token. Defaults to the VAULT_TOKEN environment variable.")
@click.option('-v', '--vaultpath', default='', help="Hashicorp's Vault path, if different from the argument.")
def decrypt(path, key, default, output, url, token, vaultpath):
    """ Decrypts credentials
        in a .ini, .conf, .json, .yml, or .yaml file.

        The PATH argument is the path to the file that contains the credentials.
        Its file type can be ommited.

        The KEY argument is the decryption key in base64 encoding.
        If ommited then the user is prompted to type one.
    """
    if not key:
        key = getpass('Encryption key: ')

    path, file_type, file_mtime = get_file_type_and_mtime(path)
    data = get_config(path, file_type, default=False)
    data = decrypt_credentials(data, key)

    # Only merge the DEFAULT section after decrypting.
    if default:
        data = merge_default(data)

    if url:
        try:
            import hvac
        except:
            print('''
To use Hashicorp's Vault you must install the hvac package.
To install it try using the following command:

  pip install hvac
''')
            exit(3)

        if not token:
            token = os.environ.get('VAULT_TOKEN', '')
            if not token:
                token = getpass('Vault token: ')
        
        client = hvac.Client(url=url, token=token)
        if not vaultpath:
            vaultpath = path

        if vaultpath[0] == '~':
            vaultpath = vaultpath[1:]
        if vaultpath[0] == '.':
            vaultpath = vaultpath[1:]
        if vaultpath[0] == '.':
            vaultpath = vaultpath[1:]
        if vaultpath[0] == '/':
            vaultpath = vaultpath[1:]

        data = merge_default(data)
        for heading in data:
            # kargs = { heading: json.dumps(data[heading]) }
            client.write(vaultpath + '/' + heading, **data[heading])

    else:

        if output:
            if output[0] == '.':
                output = output[1:]
            file_type = '.' + output.lower()

        with open(path + file_type, 'w') as save_file:
            if file_type == '.json':
                json.dump(data, save_file, indent=2)

            elif file_type in {'.ini', '.conf'}:
                if default:
                    default_section = 'DEFAULT'
                else:
                    default_section = 'DEFAULT' + os.urandom(16).hex()
                config_ini = configparser.ConfigParser(
                    dict_type=OrderedDict,
                    default_section=default_section,
                    interpolation=None)
                for heading in data:
                    config_ini.add_section(heading)
                    for item in data[heading]:
                        config_ini.set(heading, item, data[heading][item])
                config_ini.write(save_file)

            else:
                write_yaml(save_file, data)


if __name__ == "__main__":
    cli()
