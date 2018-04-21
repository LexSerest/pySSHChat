import sys
import yaml
import os
import logging

import pysshchat.variables as variables

path = os.path.dirname(__file__)
path_yaml = os.path.join(path, '../yaml')
path_commands = os.path.join(path, '../commands')


def config(path=path_yaml, file="config.yaml"):
    try:
        with open(os.path.join(path, file), 'r') as stream:
            variables.config.update(yaml.load(stream))
    except Exception as exc:
        logging.critical('Error load config.yaml file')
        sys.exit()


def text(path=path_yaml, file="texts.yaml"):
    try:
        with open(os.path.join(path, file), 'r') as stream:
            variables.texts.update(yaml.load(stream))
    except Exception as exc:
        logging.critical('Error load texts file %s' % path)
        sys.exit()


def commands(path=path_commands):
    loads = []
    for command in os.listdir(path):
        name = command[:-3]
        if command[-3:] == ".py":
            try:
                modules = __import__('pysshchat.commands.' + name, locals(), globals())
                loads.append(name)
            except Exception as error:
                logging.exception("Unable to load %s.%s" % (path, command), error)
    print('Loads commands "%s"' % ', '.join(loads))

