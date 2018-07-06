import re
import sys
import os
import asyncio
import asyncssh
import logging
import hashlib

from pathlib import Path

from pysshchat.user.ui import UI
from pysshchat.user.line import Line
from pysshchat.store import store

logging = logging.getLogger("server")


def fingerprint(key):
    fp_plain = hashlib.md5(key).hexdigest()
    return ":".join(a + b for a, b in zip(fp_plain[::2], fp_plain[1::2]))


def genkey(path):
    if not path:
        path = "~/.ssh/pysshchat"
    key_path = os.path.expanduser(path)
    path = Path(key_path)

    if not path.is_file():
        Path(path.parent).mkdir(parents=True, exist_ok=True)
        key = asyncssh.generate_private_key("ssh-rsa")
        key.write_private_key(key_path)
        print("Generate host key")
        # print("Fingerprint MD5:" + fingerprint(key.get_ssh_public_key()))
    return key_path


class MyServer(asyncssh.SSHServer):
    def connection_made(self, conn):
        self._conn = conn
        conn.is_admin = False

    def begin_auth(self, username):
        admins = store.config.get("admin", False)
        if admins:
            return bool(admins.get(username, False))

    def validate_public_key(self, username, key):
        user_key = fingerprint(key.get_ssh_public_key())
        admin_key = store.config["admin"].get(username, False)
        is_auth = user_key == admin_key

        if is_auth and not self._conn.is_admin:
            self._conn.is_admin = True

        return is_auth

    def public_key_auth_supported(self):
        return True

    def connection_lost(self, exc):
        username = self._conn.get_extra_info("username")
        user = store.users.get(username, None)
        if user:
            user.exit()


class Server:
    loop = asyncio.get_event_loop()
    pid = "/tmp/pysshchat.pid"

    def __init__(self):
        store.server = self

    async def handle_client(self, process):
        try:
            username = process.channel.get_extra_info("username")
            ip, port = process.channel.get_extra_info("peername")
            process.is_admin = ip == "127.0.0.1" or process._conn.is_admin

            if ip in store.bans.values():
                return self.error(process, "Sorry, you are banned.")

            size_x, size_y, term_x, term_y = process.get_terminal_size()
            simple_mode = process.env.get("SIMPLE", None)

            normal_mode = True
            if size_x < 60 or size_y < 15 or not len(process.env.items()):  # for mobile
                normal_mode = False
            if simple_mode:
                normal_mode = simple_mode != "1"
            if store.config.get("only_simply_mode", False):
                normal_mode = False

            username = re.sub("[^\w]", "", username)

            if not len(username):
                return self.error(process, "Empty username.")
            if len(username) > 10:
                return self.error(process, "Max username len 10 chars.")
            if username in store.users:
                return self.error(process, "This username is used.")

            password = store.config.get("password")
            if password:
                process.stdout.write("Password: ")
                try:
                    process.channel.set_echo(False)
                    line = await process.stdin.readline()
                    if line.rstrip("\n") != password:
                        return self.error(process, "Incorrect password")
                except:
                    process.close()

            process.channel.set_echo(False)
            process.channel.set_line_mode(False)

            if not normal_mode:
                Line(username, process, self.loop)
            else:
                UI(username, process, self.loop)


        except Exception as e:
            logging.exception(e)

    def info(self):
        host = store.config.get("host", "127.0.0.1")
        port = store.config.get("port", 2200)
        key = genkey(store.config.get("host_key", "~/.ssh/pysshchat"))
        print("Host key file - %s" % key)
        print("Listing %s:%s" % (host, port))

        return host, port, key

    async def start_server(self):
        host, port, key = self.info()

        await asyncssh.create_server(MyServer, host, port,
                                     server_host_keys=[key],
                                     process_factory=self.handle_client, line_editor=True)

    def error(self, process, text):
        process.stdout.write(text + "\r\n")
        process.close()

    def run(self):
        try:
            self.loop.run_until_complete(self.start_server())
        except (OSError, asyncssh.Error) as exc:
            sys.exit("Error starting server: " + str(exc))

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            tasks = [asyncio.ensure_future(user.wait_closed()) for user in store.users.values()]
            if len(tasks):
                self.loop.run_until_complete(asyncio.wait(tasks))

        except Exception as e:
            logging.exception(e)

    def start(self):
        self.run()
