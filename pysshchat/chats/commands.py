from .lib import keycode
from .globals import keysDict


keycode = keycode.__dict__
list = {}
keys = []


def register(name, isKeys=False):
    def wrap(f):
        list[name] = f
        if isKeys:
            if name in keysDict:
                if keysDict[name] in keycode:
                    keys.append((keycode[keysDict[name]], f))
                else:
                    print("%s key not found in KeyCode in keycode.py" % keysDict[name])
            else:
                print('"%s" not found register key in keys.yaml' % name)

    return wrap


def handler(user, cmd, args=[]):
    if cmd in list:
        list[cmd](user, args)


def keypress_handler(user, key):
    for o in keys:
        if key in o[0]:
            o[1](user, [])
