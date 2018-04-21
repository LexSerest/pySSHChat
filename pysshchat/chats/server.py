import asyncio
import asyncssh
import sys
import logging
import re

from pysshchat.chats.user_ui import UserUI
import pysshchat.variables as variables
from pysshchat.lib import genkey

loop = asyncio.get_event_loop()


def error(process, text):
    process.stdout.write(text + '\n')
    process.close()


async def handle_client(process):
    try:
        username = process.channel.get_extra_info('username')
        username = re.sub("[^\w]", '', username)

        if not len(username):
            return error(process, 'Empty username.')

        if len(username) > 10:
            return error(process, 'Max username len 10 chars.')

        if username in variables.users:
            return error(process, 'This username is used.')

        password = variables.config.get('password')
        if password:
            process.channel.set_echo(False)
            process.stdout.write('Password: ')
            try:
                line = await process.stdin.readline()
                if line.rstrip('\n') != password:
                    return error(process, 'Incorrect password')
            except:
                process.close()

        UserUI(username, process, loop)

    except Exception as e:
        logging.exception(e)


class MyServer(asyncssh.SSHServer):
    def begin_auth(self, username):
        return False


async def start_server():
    host = variables.config.get('host', '127.0.0.1')
    port = variables.config.get('port', 2200)
    key = genkey(variables.config.get('host_key', ''))
    print('Use host key - %s' % key)
    print('Listing %s:%s' % (host, port))

    await asyncssh.create_server(MyServer, host, port,
                                 server_host_keys=[key],
                                 process_factory=handle_client)


def run():
    try:
        loop.run_until_complete(start_server())
    except (OSError, asyncssh.Error) as exc:
        sys.exit('Error starting server: ' + str(exc))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        for name, user in variables.users.items():
            loop.run_until_complete(user.exit())
        loop.close()
