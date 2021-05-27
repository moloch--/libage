#!/usr/bin/env python3

import os
import age
import random
import unittest


ED25519_PRIVATE_KEY = b'''-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBHIICz25gBQU+Ep+5DI6mipvD9eok//BADKAvrEooJegAAAJiFNS5+hTUu
fgAAAAtzc2gtZWQyNTUxOQAAACBHIICz25gBQU+Ep+5DI6mipvD9eok//BADKAvrEooJeg
AAAEDc1uSqW6oQyKcnRAnV2PLvuO40lznsoDQBjYOn7jf4REcggLPbmAFBT4Sn7kMjqaKm
8P16iT/8EAMoC+sSigl6AAAAEXJvb3RAOTVjMGE4ZjI5ZTZiAQIDBA==
-----END OPENSSH PRIVATE KEY-----'''
ED25519_PUBLIC_KEY = b'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEcggLPbmAFBT4Sn7kMjqaKm8P16iT/8EAMoC+sSigl6 root@95c0a8f29e6b'

RSA_PRIVATE_KEY = b'''-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----'''
RSA_PUBLIC_KEY = b'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC9eTQVjqMaopSDVF5igf65bwlW4bCySNFiDojpChFMezqzTzNyT5I69eYV0gCXOrwAvNJJUAcFYq1OcEtFolRIAS7GCiL3VR1i7rTC0E6ErJWfp9bXhnvUY4f4dZBcvLHk+BSwd8sNbgzCj324+vv4B5uthbw4D+sQPwWR9CbRrceRoM91HKDgyGLV7rVXINH1Ndiw161okwTLyz2kq9m/84OZ1G5faDo5Rzs+LKqL9dTek1BBUe3TfQQWm4uX6jejNFE2HPcrGyFBU6Ao76E+GhAUlO0fsrL4Fe+StasHg/fpjEjKaPmw7ojRsRKR5TYmTbPpp5HF+jpEwYS9Blni5E8CPt05klo6AR9Qv3H+59/VGHp3XUjOE1etMsBSMo+H0p8ovL7FvwZCq1MBqYxSE7uJsbbkbgfWIJD2xxXokNl5kGmGDqSaWbkW6vFBp8wS9hSlIJ1bgyhM5hYI94mOoYTZou4ZYMLS7oJi4pxVDIoyr8YNtah4xD0fRUSKSIVxXLxYZFAlB8aA9h/pYNZsbqHHtp+MHJ0cpMa9b6sbSAcLOpOCjHDB3OJuMSnBUCRNjm3DQL3rqG7UIIEVhwVDhIyHyuMbUVCsSSDJhF+Mk7OyLXxKxL22sI0A1kq0ah8CZVgKBK8gIenpNepiVgKuDcCTyAZBy6qD9PO7WjvHqQ== root@37371dc94e2c'


hello_world = b'hello world\n'


class TestStringMethods(unittest.TestCase):

    N = 40

    def random_data(self):
        return os.urandom(random.randint(8, 8))        

    def test_encrypt(self):
        for _ in range(self.N):
            age.encrypt(RSA_PUBLIC_KEY, hello_world)

    def test_encrypt_bad_key(self):
        with self.assertRaises(age.FailedToEncrypt):
            age.encrypt("asdf", hello_world)
    
    def test_rsa_encrypt_decrypt(self):
        ciphertext = age.encrypt(RSA_PUBLIC_KEY, hello_world)
        self.assertEqual(hello_world, age.decrypt(RSA_PRIVATE_KEY, ciphertext))
        for _ in range(self.N):
            plaintext = self.random_data()
            ciphertext = age.encrypt(RSA_PUBLIC_KEY, plaintext)
            self.assertEqual(plaintext, age.decrypt(RSA_PRIVATE_KEY, ciphertext))

    # def test_ed25519_encrypt_decrypt(self):
    #     ciphertext = age.encrypt(ED25519_PUBLIC_KEY, hello_world)
    #     self.assertEqual(hello_world, age.decrypt(ED25519_PRIVATE_KEY, ciphertext))
    #     for _ in range(self.N):
    #         plaintext = self.random_data()
    #         ciphertext = age.encrypt(ED25519_PUBLIC_KEY, plaintext)
    #         self.assertEqual(plaintext, age.decrypt(ED25519_PRIVATE_KEY, ciphertext))


if __name__ == '__main__':
    unittest.main()
