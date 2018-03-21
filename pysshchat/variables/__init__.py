from queue import Queue

texts = {}
config = {}
users = {}
queue = Queue()
keysDict = {}
history = []
command_list = {}
command_keys = []


def add_history(line):
    global history
    history.append(line)
    history = history[-100:]
    #print(re.sub(r"(\^|\x1B)\[{1,2}([0-9]{1,3}(;[0-9]{1,3})*?)?[mGK]", '', line)) # used for logging?
