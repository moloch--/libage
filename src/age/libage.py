#!/usr/bin/env python3

import os
import ctypes
import platform
from typing import Union
from base64 import b64decode


DIR = os.path.dirname(os.path.abspath(__file__))
if platform.system() == "Linux":
    if platform.processor() == "arm":
        LIB_PATH = os.path.join(DIR, "libage-arm64.so")
    else:
        LIB_PATH = os.path.join(DIR, "libage.so")
if platform.system() == "Darwin":
    LIB_PATH = os.path.join(DIR, "libage.dylib")
if os.path.exists(LIB_PATH):
    AGE = ctypes.cdll.LoadLibrary(LIB_PATH)


class FailedToEncrypt(Exception):
    pass


class FailedToDecrypt(Exception):
    pass


def encrypt(public_key: Union[bytes, str], plaintext: Union[bytes, str]) -> bytes:
    """Encrypt data using public key"""
    if not os.path.exists(LIB_PATH):
        raise NotImplementedError()

    if isinstance(public_key, str):
        public_key = public_key.encode()
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()

    # Load Encrypt
    Encrypt = AGE.Encrypt
    Encrypt.argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.c_uint32]
    Encrypt.restype = ctypes.c_char_p

    # Load ResultErr
    ResultErr = AGE.ResultErr
    ResultErr.argtypes = []
    ResultErr.restype = ctypes.c_char_p

    # Load ResultLen
    ResultLen = AGE.ResultLen
    ResultLen.argtypes = []

    # Load ResultFree
    ResultFree = AGE.ResultFree
    ResultFree.argtypes = []

    resultPtr = Encrypt(public_key, plaintext, len(plaintext))
    if resultPtr is None:
        resultErr = ResultErr()
        reason = ctypes.string_at(resultErr).decode("utf-8")
        ResultFree()
        raise FailedToEncrypt(reason)

    resultLength = ResultLen()
    ciphertext = bytes(ctypes.string_at(resultPtr, resultLength))
    ResultFree()
    return ciphertext


def decrypt(private_key: Union[bytes, str], ciphertext: Union[bytes, str]) -> bytes:
    """Decrypt data using private key"""
    if not os.path.exists(LIB_PATH):
        raise NotImplementedError()

    if isinstance(private_key, str):
        private_key = private_key.encode()
    if isinstance(ciphertext, str):
        ciphertext = ciphertext.encode()

    # Load Encrypt
    Decrypt = AGE.Decrypt
    Decrypt.argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.c_uint32]
    Decrypt.restype = ctypes.c_char_p

    # Load ResultErr
    ResultErr = AGE.ResultErr
    ResultErr.argtypes = []
    ResultErr.restype = ctypes.c_char_p

    # Load ResultLen
    ResultLen = AGE.ResultLen
    ResultLen.argtypes = []

    # Load ResultFree
    ResultFree = AGE.ResultFree
    ResultFree.argtypes = []

    resultPtr = Decrypt(private_key, ciphertext, len(ciphertext))
    if resultPtr is None:
        resultErr = ResultErr()
        reason = ctypes.string_at(resultErr).decode("utf-8")
        ResultFree()
        raise FailedToDecrypt(reason)

    resultLength = ResultLen()
    # NOTE: The `ctypes.string_at` null terminates even if you pass in the desired
    # length and ctypes doesn't seem to have any decent support for just reading n
    # bytes from the address. The work around is that the Go code base64 encodes the
    # plaintext before returning it to avoid any nulls and then we decode it
    plaintext = bytes(ctypes.string_at(resultPtr, resultLength))
    ResultFree()
    return b64decode(plaintext)
