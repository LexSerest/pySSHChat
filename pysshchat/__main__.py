import sys
import argparse
import pysshchat
import pysshchat.variables as variables
from pysshchat.variables.loads import commands, text, config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", help="Hostname (default: 127.0.0.1)", nargs='?')
    parser.add_argument("-p", "--port", help="Set port listen (default: 2200)", nargs='?', type=int)
    parser.add_argument("-k", "--key", help="Host rsa key path (default auto generated in ~/.ssh/pysshchat)", nargs='?')
    parser.add_argument("--password", help="Set password for connect to chat (default non-password)", nargs='?')
    parser.add_argument("--config", help="Path config.yaml (see pysshchat/yaml/config.yaml)", nargs='?')
    parser.add_argument("--set-motd", help="Set welcome message", nargs='?')
    parser.add_argument("--set-motd-file", help="Set welcome message", nargs='?')
    parser.add_argument("--set-help", help="Set help message", nargs='?')
    parser.add_argument("--set-help-file", help="Set help message", nargs='?')
    parser.add_argument("--load-commands", help="Load commands on path", nargs='?')
    parser.add_argument("--load-text", help="Load texts.yaml on path", nargs='?')
    args = parser.parse_args()

    pysshchat.init()
    if args.host:
        variables.config['host'] = args.host

    if args.port:
        variables.config['port'] = args.port

    if args.key:
        variables.config['host_key'] = args.key

    if args.config:
        config(args.config)

    if args.password:
        variables.config['password'] = args.password

    if args.set_motd:
        variables.texts['text']['MOTD'] = args.set_motd

    if args.set_motd_file:
        try:
            with open(args.set_motd_file, 'r', encoding='utf-8') as file:
                variables.texts['text']['MOTD'] = file.read()
        except Exception as exc:
            print('Error load %s file' % args.set_motd_file)
            sys.exit()

    if args.set_help:
        variables.texts['text']['help'] = args.set_help

    if args.set_help_file:
        try:
            with open(args.set_help, 'r', encoding='utf-8') as file:
                variables.texts['text']['help'] = file.read()
        except Exception as exc:
            print('Error load %s file' % args.set_help)
            sys.exit()

    if args.load_text:
        text(args.load_text)

    if args.load_commands:
        commands(args.load_commands)

    pysshchat.run()
