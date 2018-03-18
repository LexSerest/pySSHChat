import sys
import yaml
import os
from queue import Queue
import logging
import builtins

pack_path = os.path.dirname(__file__)
logging = logging.getLogger('globals')
this = sys.modules[__name__]


this.texts = {}
this.config = {}
this.users = {}
this.queue = Queue()
this.keysDict = {}
this.history = []

from .commands import register
builtins.register = register


def add_history(line):
    this.history.append(line)
    this.history = this.history[-100:]


def get_history():
    return this.history


def loadconfig(path):
    try:
        with open(os.path.join(path, "config.yaml"), 'r') as stream:
            this.config.update(yaml.load(stream))
    except Exception as exc:
        logging.critical('Error load config.yaml file')
        sys.exit()


def loadtext(path):
    try:
        with open(os.path.join(path, "texts.yaml"), 'r') as stream:
            this.texts.update(yaml.load(stream))
    except Exception as exc:
        logging.critical('Error load texts.yaml file')
        sys.exit()


def loadkeys(path):
    try:
        with open(os.path.join(path, "keys.yaml"), 'r') as stream:
            this.keysDict.update(yaml.load(stream))
    except Exception as exc:
        logging.critical('Error load texts.yaml file')
        sys.exit()


def loadfile(path=None):
    if not path:
        path = os.path.join(pack_path, '../yaml')
    loadconfig(path)
    loadtext(path)
    loadkeys(path)


def loadcommands(path=None):
    if not path:
        path = os.path.join(pack_path, '../commands')

    loads = []
    for command in os.listdir(path):
        name = command[:-3]
        if command[-3:] == ".py":
            try:
                modules = __import__('pysshchat.commands.' + name, locals(), globals())
                loads.append(name)
            except Exception as error:
                logging.exception("Unable to load " + command, error)
    print('Loads commands "%s"' % ', '.join(loads))

