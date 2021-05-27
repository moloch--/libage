Libage
======

A shared library build of [age](https://github.com/FiloSottile/age).


### Usage

Basic example usage:

```python
import age

plaintext = b"hello world"
ciphertext = age.encrypt(public_key, plaintext)

age.decrypt(private_key, ciphertext)
```


### Supported Platforms

Windows, Linux, MacOS (Intel), however any platform that is supported by both Python and Golang in theory should be possible to support but may not work out of the box.
