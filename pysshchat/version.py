import subprocess
import re
import os
from os.path import isdir, join, dirname

PREFIX = '1.0.%s'


version_re = re.compile('^Version: (.+)$', re.M)


def get_version():
    d = dirname(__file__)

    if isdir('.git'):
        version = PREFIX % int(subprocess.check_output(['git', 'rev-list', '--all', '--count']))
        with open(join(d, '.version'), 'w') as f:
            f.write(version)

    else:
        with open(join(d, '.version'), 'r') as f:
            version = f.read()

    return version
