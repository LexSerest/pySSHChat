import logging
from pysshchat.chats.server import run as run_server

logging.basicConfig(level=logging.WARN)


def init():
    from pysshchat.variables.loads import commands, config, text

    config()
    text()
    commands()


def run():
    try:
        run_server()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception(e)


def start():
    init()
    run()


if __name__ == "__main__":
    start()

