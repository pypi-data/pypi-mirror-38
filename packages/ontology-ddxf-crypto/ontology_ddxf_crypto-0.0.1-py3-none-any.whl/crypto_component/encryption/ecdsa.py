#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ecdsa.curves import SECP256k1

from ecdsa.ellipticcurve import Point

from ecdsa.util import (
    string_to_number,
    number_to_string
)

from ecdsa.keys import (
    SigningKey,
    VerifyingKey,
    BadSignatureError
)

from crypto_component.exception.crypto_exception import (
    CryptoError,
    CryptoException
)


class ECDSA:
    @staticmethod
    def generate_private_key():
        private_key = SigningKey.generate(SECP256k1)
        return private_key.to_string()

    @staticmethod
    def ec_get_public_key_by_private_key(private_key: bytes):
        if not isinstance(private_key, bytes):
            raise CryptoException(CryptoError.invalid_private_key)
        if len(private_key) != 32:
            raise CryptoException(CryptoError.invalid_private_key)
        private_key = SigningKey.from_string(string=private_key, curve=SECP256k1)
        public_key = private_key.get_verifying_key().to_string()
        return public_key

    @staticmethod
    def generate_signature(private_key: bytes, msg: bytes):
        if not isinstance(private_key, bytes):
            raise CryptoException(CryptoError.invalid_private_key)
        if len(private_key) != 32:
            raise CryptoException(CryptoError.invalid_private_key)
        private_key = SigningKey.from_string(string=private_key, curve=SECP256k1)
        signature = private_key.sign(msg)
        return signature

    @staticmethod
    def verify_signature(public_key: bytes, signature: bytes, msg: bytes):
        if not isinstance(public_key, bytes):
            raise CryptoException(CryptoError.invalid_public_key)
        if len(public_key) != 64:
            raise CryptoException(CryptoError.invalid_public_key)
        public_key = VerifyingKey.from_string(string=public_key, curve=SECP256k1)
        try:
            result = public_key.verify(signature, msg)
        except BadSignatureError:
            result = False
        return result
