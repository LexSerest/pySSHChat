import subprocess
from setuptools import setup, find_packages
from os.path import isdir, join, dirname

PREFIX = "2.1.%s"


def get_version():
    d = dirname(__file__)
    if isdir(".git"):
        version = PREFIX % int(subprocess.check_output(["git", "rev-list", "--all", "--count"]))
        with open(join(d, ".version"), "w") as f:
            f.write(version)
    else:
        with open(join(d, ".version"), "r") as f:
            version = f.read()

    return version


setup(
    name="pySSHChat",
    packages=find_packages(),
    version=get_version(),
    description="SSH chat server written on Python3",
    author="LexSerest",
    author_email="lexserest@gmail.com",
    url="https://github.com/LexSerest/pySSHChat/",
    keywords=["ssh", "chat", "ssh chat"],
    install_requires=[
        "pyyaml",
        "asyncssh",
        "urwid",
        "sty",
        "aiohttp"
    ],
    include_package_data=True,
    license="MIT",
    scripts=['bin/pysshchat']
)
