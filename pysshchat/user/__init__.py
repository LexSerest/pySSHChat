import datetime
import re
import logging
import random
import threading

from pysshchat.store import store
from pysshchat.commands import handler


logging = logging.getLogger("pysshchat.user")

class UserBase(object):
    def __init__(self, username, process, loop):
        ip, port = process.channel.get_extra_info("peername")
        self.ip = ip
        self.connected_date = datetime.datetime.now()
        self.title = store.dotget("text.title")
        self.username = username
        self.process = process
        self.is_admin = process.is_admin
        self.loop = loop
        self.color = False
        self.color = str(random.randint(1, 254))
        self.connected = True
        self.admin = False
        self.event_join()

    def send(self, type="format.msg", text="", me=True):
        store.history.add(self.format(type, text=text, u=self))
        for user in store.users.values():
            if not me and user == self:
                continue
            user.local(type=type, text=text, u=self)

    def local(self, type="format.text", **kwargs):
        self.message_print(type, **kwargs)

    def change_color(self, color=False):
        if not color:
            self.color = str(random.randint(1, 254))
        else:
            self.color = color

    def exit(self):
        self.connected = False
        try:
            self.event_quit()
            self.process.close()
        except Exception as e:
            logging.exception(e)

    async def wait_closed(self):
        self.exit()
        await self.process.wait_closed()

    def message_print(self, type, **kwargs):
        pass

    def format(self, key, **kwargs):
        kwargs["time"] = datetime.datetime.now().strftime("%H:%M")
        if not kwargs.get("u", None):
            kwargs["u"] = self

        text = store.dotget(key).format(**kwargs)
        return text

    def text_format(self, key, **kwargs):
        pattern = r"#(.+?)#"

        if not kwargs.get("off_formatting", False):
            key = self.format(key, **kwargs)

        return re.split(pattern, key)

    def event_join(self):
        self.send(type="messages.connect")
        store.users[self.username] = self

        for user in store.users.values():
            if user != self:
                user.event_join_another()

    def event_join_another(self):
        pass

    def event_quit(self):
        self.connected = False
        store.users.pop(self.username)
        self.send(type="messages.disconnect", me=False)

        for user in store.users.values():
            user.event_quit_another()

    def event_quit_another(self):
        pass

    def event_key(self, key):
        handler(self, key)

    def event_key_enter(self, text):
        try:
            if text:
                if text[0] == "/":
                    cmd = text[1:].split(" ")
                    handler(self, cmd=cmd[0], args=cmd[1:])
                else:
                    self.send(text=text)
        except Exception as e:
            logging.exception(e)

    def event_key_tab(self, text):
        pass

    def load_history(self):
        for line in store.history.get():
            self.local(line, off_formatting=True)

