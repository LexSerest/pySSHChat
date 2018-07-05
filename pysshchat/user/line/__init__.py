import asyncssh
import sty
import re

from urwid.escape import process_keyqueue

from pysshchat.user import UserBase
from pysshchat.store import store

users = store.users


class Line(UserBase):
    text = ""
    cursor = 0

    def __init__(self, username, process, loop):
        super().__init__(username, process, loop)
        self.prompt = self.text_format("format.prompt", u=self)
        loop.create_task(self.run())
        self.load_history()

    async def run(self):
        self.clear_input(True)
        self.set_input()

        self.local("text.title")

        while self.connected:
            t = ""
            key = ""

            try:
                t = await self.process.stdin.read(5)
            except asyncssh.BreakReceived:
                continue
            except asyncssh.misc.TerminalSizeChanged:
                continue
            except KeyboardInterrupt:
                break

            if not t:
                continue

            key = process_keyqueue(t.encode("utf-8"), True)[0][0]

            if len(key) == 1:       # wtf? u a crazy
                if len(self.text) < 100:
                    self.text += t
                    self.cursor += 1
                    self.write(t)

            elif key in ("ctrl d", "ctrl c"):
                self.exit()

            elif key == "backspace":
                if self.text:
                    self.text = self.text[:-1]
                    self.write("\b \b")

            elif key == "ctrl w":
                self.clear_input(True)
                self.set_input()

            elif key == "enter":
                if self.text.strip():
                    super().event_key_enter(self.text.strip())
                    self.clear_input()
                    self.set_input()
            elif key == "tab":
                if self.text.strip():
                    self.event_key_tab(self.text.strip())
            else:
                super().event_key(key)

    def message_print(self, type, **kwargs):
        text = self.text_format(type, **kwargs)
        self.add_line(text)
        return text

    def text_format(self, key, **kwargs):
        out = ""

        texts = super().text_format(key, **kwargs)
        out += texts[0]

        colors = texts[1::2]
        for index, text in enumerate(texts[2::2]):
            color = colors[index]
            if text:
                if color == "-":
                    out += sty.rs.all + text
                elif color == "b":
                    out += sty.ef.bold + text
                elif color == "i":
                    out += sty.ef.italic + text
                elif color == "info":
                    out += sty.ef.bold + sty.bg.cyan + sty.fg.white + text
                else:
                    if color.isdigit():
                        out += sty.fg(int(color)) + text
                    else:
                        out += text


        out += sty.rs.all
        return out.replace("\n", "\r\n")

    def write(self, text):
        try:
            self.process.stdout.write(text)
        except BrokenPipeError:
            pass

    def clear_input(self, cls=False):
        # ohh, this is indian code. how delete spec symbols?
        msg_len = len(re.sub(r"(\^|\x1B)\[{1,2}([0-9]{1,3}(;[0-9]{1,3})*?)?[mGK]", "", self.prompt + self.text))

        size_x, size_y, term_x, term_y = self.process.get_terminal_size()
        self.write("\r\033[K")          # clear line
        for i in range(0, msg_len // size_x):
            self.write("\033[F")        # up cursor
            self.write("\r\033[K")
        if cls:
            self.text = ""

    def set_input(self, text=""):
        self.write(self.prompt + text)

    def add_line(self, msg):
        self.clear_input(True)
        self.write("\r%s\r\n" % msg)
        self.set_input(self.text)

    def change_color(self, color=False):
        super().change_color(color)
        self.prompt = self.text_format("format.prompt", u=self)
        self.clear_input(True)
        self.set_input()

    def event_key_tab(self, text):
        args = text.split(" ")
        text = args[-1]
        keys = store.users.keys()

        if text[0] == "/":
            keys = store.get_commands_list(self.is_admin)
            text = text[1:]

        users_find = [u for u in keys if u.startswith(text)]
        if len(users_find):
            w = users_find[0][len(text):]
            self.write(w)
            self.text += w