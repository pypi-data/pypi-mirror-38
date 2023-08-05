# -*- coding: utf-8 -*-

""" Abstract away the usage of encryption libraries.
"""

from __future__ import print_function, division, unicode_literals

import json

from math import ceil
from collections import OrderedDict
from base64 import b64encode, b64decode


KEY_BIT_LENGTH = 256
NONCE_BIT_LENGTH = 96
NON_CONFIDENTIAL_ASSOCIATED_DATA = 'eas{}gcm{}'.format(KEY_BIT_LENGTH, NONCE_BIT_LENGTH).encode('utf-8')


try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.exceptions import InvalidTag
    from os import urandom as get_random_bytes

    def generate_key(bit_length=KEY_BIT_LENGTH):
        return AESGCM.generate_key(bit_length=bit_length)

    def encrypt(key, nonce, data):
        aesgcm = AESGCM(key)
        encrypted = aesgcm.encrypt(nonce, data, NON_CONFIDENTIAL_ASSOCIATED_DATA)
        return encrypted

    def decrypt(key, nonce, data):
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, data, NON_CONFIDENTIAL_ASSOCIATED_DATA)

except:
    # In case we need to use this pure python PyCrypto forked library:
    # https://github.com/Legrandin/pycryptodome
    try:
        from Crypto.Cipher import AES
        MODE_GCM = AES.MODE_GCM
        from Crypto.Random import get_random_bytes
    except:
        try:
            from Cryptodome.Cipher import AES
            MODE_GCM = AES.MODE_GCM
            from Cryptodome.Random import get_random_bytes

            def generate_key(bit_length=KEY_BIT_LENGTH):
                return get_random_bytes(bit_length // 8)

            def encrypt(key, nonce, data):
                aesgcm = AES.new(key, MODE_GCM, nonce)
                aesgcm.update(NON_CONFIDENTIAL_ASSOCIATED_DATA)
                encrypted = aesgcm.encrypt(data)
                return encrypted

            def decrypt(key, nonce, data):
                aesgcm = AES.new(key, MODE_GCM, nonce=nonce)
                aesgcm.update(NON_CONFIDENTIAL_ASSOCIATED_DATA)
                return aesgcm.decrypt(data)
        except:
            print('''
You must install one of the following encryption packages:

  conda install cryptography
    or
  pip install cryptography
    or
  pip install pycryptodome
    or
  pip install pycryptodomex
''')
            exit(2)


def encrypt_credentials(data, key=None):
    if not key:
        key = generate_key(KEY_BIT_LENGTH)
        print('The encryption key is: ' + b64encode(key).decode('utf8').rstrip('='))
    else:
        key += '=' * ((4 - len(key) % 4) % 4)
        key = b64decode(key.encode('utf8'))

    new_data = dict()

    for item in data:
        item_data = data[item]
        if type(item_data) != OrderedDict or 'encrypted' not in item_data:
            to_encrypt = json.dumps(item_data, separators=(',', ':')).encode('utf8')
            
            nonce = get_random_bytes(int(ceil(NONCE_BIT_LENGTH / 8.0)))
            encrypted = encrypt(key, nonce, to_encrypt)

            new_data[item] = {
                'encrypted':
                    b64encode(encrypted).decode('utf8').rstrip('=') +
                    b64encode(nonce).decode('utf8').rstrip('='),
            } 
        else:
            new_data[item] = item_data

    return new_data


def decrypt_credentials(data, key):
    key += '=' * ((4 - len(key) % 4) % 4)
    key = b64decode(key.encode('utf8'))
        
    new_data = dict()

    for item in data:
        item_data = data[item]
        if type(item_data) == OrderedDict and 'encrypted' in item_data:

            encoded_nonce_byte_len = int(ceil(NONCE_BIT_LENGTH / 6.0))
            nonce = item_data['encrypted'][-encoded_nonce_byte_len:]  
            nonce += '=' * ((4 - encoded_nonce_byte_len % 4) % 4)
            nonce = b64decode(nonce.encode('utf8'))

            to_decrypt = item_data['encrypted'][:-encoded_nonce_byte_len]
            to_decrypt += '=' * ((4 - len(to_decrypt) % 4) % 4)
            to_decrypt = b64decode(to_decrypt.encode('utf8'))

            try:
                decrypted_bytes = decrypt(key, nonce, to_decrypt)
            except:
                print('Error: Wrong encryption key.')
                exit(1)
            
            new_data[item] = json.loads(decrypted_bytes.decode('utf8'))
        else:
            new_data[item] = item_data

    return new_data
