import pysshchat.variables as variables


def register(name, key=None):
    def wrap(f):
        variables.command_list[name] = f
        if key:
            variables.command_keys.append((key, f))
    return wrap


def handler(user, cmd, args=[]):
    if cmd in variables.command_list:
        variables.command_list[cmd](user, args)


def keypress_handler(user, key):
    for o in variables.command_keys:
        if key in o[0]:
            o[1](user, [])
