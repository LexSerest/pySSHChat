__version__ = '1.0.0'

import logging
logging.basicConfig(level=logging.WARN)


from pysshchat.chats.globals import loadcommands, loadfile
from pysshchat.chats.globals import texts, config

def init():
    loadfile()
    loadcommands()


def run():
    from pysshchat.chats.server import start, chatstream
    try:
        chatstream()
        start()
    except KeyboardInterrupt as e:
        from pysshchat.chats.events import server_down
        server_down()
    except Exception as e:
        logging.exception(e)


def start():
    init()
    run()


if __name__ == "__main__":
    start()


