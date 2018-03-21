import logging

import pysshchat.variables as variables
from pysshchat.lib.host_key import genkey
from pysshchat.chats import start as server_start, chatstream
from pysshchat.variables.loads import commands, config, keys, text

logging.basicConfig(level=logging.CRITICAL)


def init():
    config()
    keys()
    text()
    commands()


def run():
    try:
        chatstream()
        server_start()
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


