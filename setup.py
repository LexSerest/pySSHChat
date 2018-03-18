from setuptools import setup, find_packages

setup(
    name='pySSHChat',
    packages=find_packages(),
    version='1.0.0',
    description='SSH chat server written on Python3',
    author='LexSerest',
    author_email='lexserest@gmail.com',
    url='https://github.com/LexSerest/pySSHChat/',
    keywords=['ssh', 'chat', 'sshchat'],
    install_requires=[
        'paramiko',
        'sty',
        'pyyaml'
    ],
    license='MIT',
    entry_points={
        'console_scripts':
            ['start = pysshchat:start']
        }
)
