import pysshchat.variables as variables
from pysshchat.lib import keycode

keycode = keycode.__dict__


def register(name, isKeys=False):
    def wrap(f):
        variables.command_list[name] = f
        if isKeys:
            if name in variables.keysDict:
                if variables.keysDict[name] in keycode:
                    variables.command_keys.append((keycode[variables.keysDict[name]], f))
                else:
                    print("%s key not found in KeyCode in keycode.py" % variables.keysDict[name])
            else:
                print('"%s" not found register key in keys.yaml' % name)
    return wrap


def handler(user, cmd, args=[]):
    if cmd in variables.command_list:
        variables.command_list[cmd](user, args)


def keypress_handler(user, key):
    for o in variables.command_keys:
        if key in o[0]:
            o[1](user, [])
