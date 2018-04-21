texts = {}
config = {}
users = {}
history = []
command_list = {}
command_keys = []


def add_history(line):
    global history
    history.append(line)
    history = history[-100:]
