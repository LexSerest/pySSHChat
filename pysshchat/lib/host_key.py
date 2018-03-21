import os
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import hashlib
import base64


def genkey(path='~/.ssh/pysshchat'):

    key_path = os.path.expanduser(path)
    path = Path(key_path)

    if not path.is_file():
        Path(path.parent).mkdir(parents=True, exist_ok=True)
        key = rsa.generate_private_key(backend=default_backend(),
                                       public_exponent=65537,
                                       key_size=2048)
        pem = key.private_bytes(encoding=serialization.Encoding.PEM,
                                format=serialization.PrivateFormat.TraditionalOpenSSL,
                                encryption_algorithm=serialization.NoEncryption())

        with open(key_path, 'w') as out:
            out.write(pem.decode('utf-8'))
        print('Generate host key')
    return key_path
