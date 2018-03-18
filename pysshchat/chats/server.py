import logging
import socket
import sys
import paramiko
import os

from .globals import config, users, queue, texts, add_history
from .interface import Server
from .client import Client
from .lib import run_thread

path = os.path.dirname(__file__)
logging = logging.getLogger('server')

@run_thread
def chatstream():
    while True:
        try:
            msg = queue.get()
            if msg is None:
                continue
            global history
            add_history(msg)
            for user in list(users):
                if user and users[user] and not users[user].closed:
                    users[user].local(msg)

        except Exception as e:
            logging.exception(e)


def start():
    try:
        global sock
        port = config.get('port', 2200)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', port))
        print('Listen %s port' % port)

    except:
        logging.warning('*** Bind %s port failed ' % (config['port']))
        sys.exit(1)

    while sock is not None:
        try:
            sock.listen(1000)
            client, addr = sock.accept()
        except Exception as e:
            print('*** Listen/accept failed: ' + str(e))
            continue

        t = paramiko.Transport(client)
        try:
            t.load_server_moduli()
        except:
            print('(Failed to load moduli -- gex will be unsupported.)')
            continue
        t.add_server_key(paramiko.RSAKey(filename=config['host_key'].format(path=path)))
        server = Server()
        try:
            t.start_server(server=server)
        except paramiko.SSHException as e:
            t.close()
            continue
        except:
            t.close()
            continue

        chan = t.accept(20)
        nick = t.get_username()
        if nick in users:
            chan.send(texts['error'].get('nick_used', 'You nick is used') + '\r\n')
            chan.close()
            continue

        if len(nick) == 0 or len(nick) > 10:
            chan.send(texts['error'].get('nick_long', 'You nick is long') + '\r\n')
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
