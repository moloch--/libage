#!/usr/bin/env python3

import os
import sys
import ctypes

SO_PATH = './libage.so'

def encrypt(public_key: str, plaintext: str) -> str:
    ''' Encrypt data using public key '''
    if not os.path.exists(SO_PATH):
        raise NotImplementedError()

    libage = ctypes.cdll.LoadLibrary(SO_PATH)

    # Load Encrypt
    Encrypt = libage.Encrypt
    Encrypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    Encrypt.restype = ctypes.c_char_p

    # Load FreeResult
    FreeResult = libage.FreeResult
    FreeResult.argtypes = []

    ptr = Encrypt(public_key, plaintext)
    ciphertext = ctypes.string_at(ptr).decode('utf-8')

    # Free result ptr
    FreeResult()

    return ciphertext


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as fp:
        public_key = fp.read()
    with open(sys.argv[2], 'rb') as fp:
        plaintext = fp.read()
    print("Public Key = %r" % public_key)
    print("Plaintext = %r" % plaintext)
    print("Ciphertext = %r" % encrypt(public_key, plaintext))
