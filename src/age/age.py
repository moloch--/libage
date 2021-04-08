#!/usr/bin/env python3

import os
import sys
import ctypes
import platform
from typing import Union


DIR = os.path.dirname(os.path.abspath(__file__))
if platform.system() == 'Linux':
    LIB_PATH = os.path.join(DIR, 'libage.so')
if platform.system() == 'Darwin':
    LIB_PATH = os.path.join(DIR, 'libage.dylib')
AGE = ctypes.cdll.LoadLibrary(LIB_PATH)


def encrypt(public_key: Union[bytes, str], plaintext: Union[bytes, str]) -> str:
    ''' Encrypt data using public key '''
    if not os.path.exists(LIB_PATH):
        raise NotImplementedError()
    if isinstance(public_key, str):
        public_key = public_key.encode()
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()

    # Load Encrypt
    Encrypt = AGE.Encrypt
    Encrypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    Encrypt.restype = ctypes.c_char_p

    # Load FreeResult
    FreeResult = AGE.FreeResult
    FreeResult.argtypes = []

    ptr = Encrypt(public_key, plaintext)
    ciphertext = ctypes.string_at(ptr).decode('utf-8')

    # Free result ptr
    FreeResult()

    return ciphertext


def decrypt(private_key: Union[bytes, str], ciphertext: Union[bytes, str]) -> bytes:
    ''' Decrypt data using private key '''
    if not os.path.exists(LIB_PATH):
        raise NotImplementedError()
    if isinstance(private_key, str):
        private_key = private_key.encode()
    if isinstance(ciphertext, str):
        ciphertext = ciphertext.encode()

    # Load Encrypt
    Decrypt = AGE.Decrypt
    Decrypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    Decrypt.restype = ctypes.c_char_p

    # Load FreeResult
    FreeResult = AGE.FreeResult
    FreeResult.argtypes = []

    ptr = Decrypt(private_key, ciphertext)
    plaintext = ctypes.string_at(ptr)

    # Free result ptr
    FreeResult()

    return plaintext


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as fp:
        public_key = fp.read()
    with open(sys.argv[2], 'rb') as fp:
        plaintext = fp.read()
    print("Public Key = %r" % public_key)
    print("Plaintext = %r" % plaintext)
    print("Ciphertext = %r" % encrypt(public_key, plaintext))
