import logging
import socket
import sys
import paramiko
import os
import pysshchat.variables as variables

from .interface import Server
from .client import Client
from pysshchat.lib import run_thread
from pysshchat.lib.host_key import genkey

host_key = variables.config.get('host_key', None)
path = os.path.dirname(__file__)
logging = logging.getLogger('server')

@run_thread
def chatstream():
    while True:
        try:
            msg = variables.queue.get()
            if msg is None:
                continue
            variables.add_history(msg)
            for user in list(variables.users):
                if user and variables.users[user] and not variables.users[user].closed:
                    variables.users[user].local(msg)

        except Exception as e:
            logging.exception(e)


def start():
    global host_key

    if not host_key:
        host_key = genkey()

    print('Host key file - %s' % host_key)

    try:
        global sock
        port = variables.config.get('port', 2200)
        host = variables.config.get('host', '127.0.0.1')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        print('Listen %s:%s' % (host, port))

    except:
        print('*** Bind %s port failed ' % (variables.config['port']))
        sys.exit(1)

    while sock is not None:
        try:
            sock.listen(1000)
            client, addr = sock.accept()
        except Exception as e:
            continue

        t = paramiko.Transport(client)
        try:
            t.load_server_moduli()
        except:
            continue

        t.add_server_key(paramiko.RSAKey(filename=host_key))
        server = Server()
        try:
            t.start_server(server=server)
        except paramiko.SSHException as e:
            t.close()
            continue
        except Exception as e:
            t.close()
            continue

        chan = t.accept(20)
        nick = t.get_username()
        if nick in variables.users:
            chan.send(variables.texts['error'].get('nick_used', 'You nick is used') + '\r\n')
            chan.close()
            continue

        if len(nick) == 0 or len(nick) > 10:
            chan.send(variables.texts['error'].get('nick_long', 'You nick is long') + '\r\n')
            chan.close()
            continue

        chan.set_name(nick)
        if chan is not None:
            server.event.wait(10)
            if not server.event.is_set():
                logging.info('*** Client never asked for a shell.')
                continue
            else:
                Client(chan)
