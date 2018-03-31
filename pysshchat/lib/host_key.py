import os
from pathlib import Path
from Crypto.PublicKey import RSA


def genkey(path='~/.ssh/pysshchat'):

    key_path = os.path.expanduser(path)
    path = Path(key_path)

    if not path.is_file():
        Path(path.parent).mkdir(parents=True, exist_ok=True)
        pem = RSA.generate(2048)
        with open(key_path, 'w') as out:
            out.write(pem.decode('utf-8'))
        print('Generate host key')
    return key_path
