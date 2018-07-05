import sys
import yaml
import os
import logging
import datetime

from functools import reduce


class History:
    def __init__(self, count=100):
        self.count = count
        self.__line = []

    def add(self, data):
        self.__line.append(data)
        self.__line = self.__line[-self.count:]

    def get(self):
        return self.__line


class Store:
    texts = {}
    config = {}
    users = {}
    history = History()
    command_list = []
    bans = {}
    server = None

    def __init__(self):
        self.load_config()
        self.load_text()

    def get_commands_list(self, is_admin=False):
        if is_admin:
            return [name[0] for name in self.command_list]
        return [name[0] for name in self.command_list if not name[3]]

    def load_config(self, path=None):
        if not path:
            path = os.path.dirname(__file__)
            path = os.path.join(path, "./yaml/config.yaml")
        try:
            with open(path, "r") as stream:
                self.config.update(yaml.load(stream))
        except Exception as exc:
            logging.critical("Error load config.yaml file")
            sys.exit()

    def load_text(self, path=None):
        if not path:
            path = os.path.dirname(__file__)
            path = os.path.join(path, "./yaml/texts.yaml")
        try:
            with open(path, "r") as stream:
                self.texts.update(yaml.load(stream))
        except Exception as exc:
            logging.critical("Error load texts file %s" % path)
            sys.exit()

    def dotget(self, key):
        try:
            return reduce(lambda c, k: c[k], key.split("."), self.texts)
        except:
            print("Not found texts.yaml key %s" % key)
            return ""


store = Store()
