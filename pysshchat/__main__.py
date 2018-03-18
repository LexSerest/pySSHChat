import sys
import argparse
import pysshchat
from pysshchat.chats.globals import texts, config, loadcommands, loadtext, loadconfig


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Set port listen (default: 2200)", nargs='?', type=int)
    parser.add_argument("-k", "--key", help="Host rsa key path)", nargs='?')
    parser.add_argument("--config", help="Path config.yaml", nargs='?')
    parser.add_argument("--set-motd", help="Set welcome message", nargs='?')
    parser.add_argument("--set-motd-file", help="Set welcome message", nargs='?')
    parser.add_argument("--set-help", help="Set help message", nargs='?')
    parser.add_argument("--set-help-file", help="Set help message", nargs='?')
    parser.add_argument("--load-commands", help="Load commands on path", nargs='?')
    parser.add_argument("--load-text", help="Load texts.yaml", nargs='?')
    args = parser.parse_args()

    pysshchat.init()
    if args.port:
        config['port'] = args.port

    if args.key:
        config['host_key'] = args.key

    if args.config:
        loadconfig(args.config)

    if args.load_commands:
        loadcommands(args.load_commands)

    if args.set_motd:
        texts['text']['MOTD'] = args.set_motd

    if args.set_motd_file:
        try:
            with open(args.set_motd_file, 'r', encoding='utf-8') as file:
                texts['text']['MOTD'] = file.read()
        except Exception as exc:
            print('Error load %s file' % args.set_motd_file)
            sys.exit()

    if args.set_help:
        texts['text']['help'] = args.set_help

    if args.set_help:
        try:
            with open(args.set_help, 'r', encoding='utf-8') as file:
                texts['text']['help'] = file.read()
        except Exception as exc:
            print('Error load %s file' % args.set_help)
            sys.exit()

    if args.load_text:
        loadtext(args.load_text)

    pysshchat.run()
