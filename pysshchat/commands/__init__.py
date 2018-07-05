import os
import logging
import asyncio
import inspect
from pysshchat.store import store

logging = logging.getLogger("commands")
command_list = store.command_list

loop = asyncio.get_event_loop()


def register(name, key=None, is_admin=False):
    def wrap(f):
        command_list.append((name, key, f, is_admin))
    return wrap


def handler(user, key=False, cmd=False, args=[]):
    try:
        for c_cmd, c_key, f, is_admin in command_list:
            if (key and key == c_key) or (cmd and cmd == c_cmd):
                if (is_admin and user.is_admin) or not is_admin:
                    if inspect.iscoroutinefunction(f):
                        asyncio.ensure_future(f(user, args))
                    else:
                        f(user, args)
    except Exception as e:
        logging.exception(e)


def load_commands():
    path = os.path.dirname(__file__)
    for command in os.listdir(os.path.join(path, "../commands")):
        name = command[:-3]
        if command[-3:] == ".py" and command[:2] != "__":
            try:
                modules = __import__("pysshchat.commands." + name, locals(), globals())
            except Exception as error:
                logging.exception(error)
