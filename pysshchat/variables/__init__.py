texts = {}
config = {}
users = {}
history = []
command_list = {}
command_keys = []


def _get_text(line):
    txt = ""
    if type(line) == str:
        txt += line
    else:
        for e in line:
            txt += e[1]
    return txt


def add_history(line):
    global history
    history.append(line)
    history = history[-100:]
    #print(_get_text(line))
