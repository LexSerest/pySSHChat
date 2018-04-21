import logging

logging.basicConfig(level=logging.WARN)


def init():
    from pysshchat.variables.loads import commands, config, text

    config()
    text()
    commands()


def run():
    from pysshchat.chats.server import run
    try:
        run()
    except KeyboardInterrupt as e:
        pass
    except Exception as e:
        logging.exception(e)


def start():
    init()
    run()


if __name__ == "__main__":
    start()

