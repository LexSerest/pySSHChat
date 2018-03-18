from ..globals import queue
import time


def server_down():
    queue.put('Server is down')
    time.sleep(1)
