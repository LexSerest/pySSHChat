import sys
import argparse
import logging

from pysshchat.store import store
from pysshchat.commands import load_commands
from pysshchat.server import Server

logging.basicConfig(level=logging.WARN)

config = store.config
texts = store.texts
server = Server()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", help="Hostname (default: 127.0.0.1)", nargs="?")
    parser.add_argument("-p", "--port", help="Set port listen (default: 2200)", nargs="?", type=int)
    parser.add_argument("-k", "--key", help="Host rsa key path (default auto generated in ~/.ssh/pysshchat)", nargs="?")
    parser.add_argument("--password", help="Set password for connect to chat (default non-password)", nargs="?")
    parser.add_argument("--config", help="Path config.yaml (see pysshchat/yaml/config.yaml)", nargs="?")
    parser.add_argument("--set-title", help="Set title chat", nargs="?")
    parser.add_argument("--set-help", help="Set help message", nargs="?")
    parser.add_argument("--set-help-file", help="Set help message", nargs="?")
    parser.add_argument("--load-text", help="Load texts.yaml on path", nargs="?")
    parser.add_argument("--only-simply-mode", dest="only_simply_mode", action="store_true", help="Only line mode (without urwid)")
    parser.set_defaults(only_simply_mode=False)
    args = parser.parse_args()

    load_commands()

    if args.host:
        config["host"] = args.host

    if args.port:
        config["port"] = args.port

    if args.key:
        config["host_key"] = args.key

    if args.password:
        config["password"] = args.password

    if args.set_title:
        texts["text"]["title"] = args.set_title

    if args.set_help:
        texts["text"]["help"] = args.set_help

    if args.only_simply_mode:
        config["only_simply_mode"] = True

    if args.set_help_file:
        try:
            with open(args.set_help, "r", encoding="utf-8") as file:
                texts["text"]["help"] = file.read()
        except Exception:
            print("Error load %s file" % args.set_help)
            sys.exit(0)

    if args.config:
        store.load_config(args.config)

    if args.load_text:
        store.load_text(args.load_text)


def start():
    server.start()


