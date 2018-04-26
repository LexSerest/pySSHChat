from setuptools import setup, find_packages
from pysshchat.version import get_version



setup(
    name='pySSHChat',
    packages=find_packages(),
    version=get_version(),
    description='SSH chat server written on Python3',
    author='LexSerest',
    author_email='lexserest@gmail.com',
    url='https://github.com/LexSerest/pySSHChat/',
    keywords=['ssh', 'chat', 'ssh chat'],
    install_requires=[
        'pyyaml',
        'pycrypto',
        'asyncssh',
        'urwid',
        'daemonize'
    ],
    include_package_data=True,
    license='MIT',
    entry_points={
        'console_scripts':
            ['start = pysshchat:start']
        }
)
