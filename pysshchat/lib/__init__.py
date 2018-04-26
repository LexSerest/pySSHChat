import os
from pathlib import Path
from Crypto.PublicKey import RSA

import threading
import logging

logging = logging.getLogger('lib')


def genkey(path):

    if not path:
        path = '~/.ssh/pysshchat'

    key_path = os.path.expanduser(path)
    path = Path(key_path)

    if not path.is_file():
        Path(path.parent).mkdir(parents=True, exist_ok=True)
        key = RSA.generate(2048)
        private = key.exportKey('PEM')
        public = key.publickey().exportKey('PEM')

        with open(key_path, 'w') as out:
            out.write(private.decode())
        # with open(key_path+'.pub', 'w') as out:
        #     out.write(public.decode())
        print('Generate host key')
    return key_path
