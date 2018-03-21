import pysshchat.variables as variables
import time


def server_down():
    variables.queue.put('Server is down')
    time.sleep(1)
