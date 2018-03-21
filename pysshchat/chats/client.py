import logging
import time
import sty
from random import randint
import pysshchat.variables as variables
from .events import keypress, left_user, new_user
from pysshchat.lib import dotget
from pysshchat.lib import run_thread
from pysshchat.lib import keycode

logging = logging.getLogger('client')


class Client:
    def __init__(self, channel):
        self.channel = channel
        self.nick = channel.get_name()
        self.color = ''
        self.text = ''
        self.prompt = ''
        self.closed = False
        self.set_color()
        self.stream()
        self.clear_input()
        self.set_input()
        self.connect()

    @run_thread
    def connect(self):
        self._send('', 'messages.connect')
        time.sleep(0.1)
        variables.users[self.nick] = self
        new_user(self)

    @run_thread
    def stream(self):
        while not self.closed:
            if self.channel.active and not self.channel.closed:
                try:
                    self.keypress()
                except Exception as e:
                    logging.info('Error keypress: %s - %s' % (self.nick, e))
                    self.close()
                    break
            else:
                self.close()
                break

    def set_color(self, color=None):
        if not color:
            color = sty.fg(randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.prompt = self.parse('format.prompt', nick=self.nick)

    def clear_input(self):
        msg_len = len(self.prompt) + len(self.text)
        self.channel.send('\r')
        self.channel.send(' ' * msg_len)
        self.channel.send('\r')

    def reset_input(self):
        self.text = ''
        self.clear_input()
        self.set_input()

    def set_input(self, text=""):
        self.channel.send(self.prompt)
        if text:
            self.channel.send(text)

    def keypress(self):
        byte = self.channel.recv(10)
        char = byte.decode("utf-8", 'ignore')
        if char.isprintable():
            self.text += char
            self.channel.send(char)
        else:
            if byte in keycode.KEY_BACKSPACE and len(self.text):
                self.channel.send('\b \b')
                self.text = self.text[:-1]
            keypress(self, byte)

    def add_line(self, msg):
        self.clear_input()
        text = self.text
        self.channel.send(msg+'\r\n')
        self.set_input(text)

    def _send(self, msg, format=None, **kwargs):
        if not format:
            variables.queue.put(msg)
        else:
            f = self.parse(format, msg=msg, **kwargs)
            variables.queue.put(f)

    def send(self):
        self._send(self.text, 'format.msg')
        self.text = ''

    def local(self, msg, format=None, **kwargs):
        if not format:
            self.add_line(msg.replace('\n', '\r\n'))
        else:
            self.add_line(self.parse(format, msg=msg, **kwargs).replace('\n', '\r\n'))

    def close(self):
        self._send('', 'messages.disconnect')
        self.closed = True
        self.channel.close()
        variables.users.pop(self.nick, None)
        left_user(self)

    def parse(self, format, **kwargs):
        d = dict(kwargs)
        d['bg'] = sty.bg
        d['ef'] = sty.ef
        d['rs'] = sty.rs
        d['fg'] = sty.fg
        d['user'] = self
        d['time'] = time.strftime("%H:%M")

        f = dotget(format, variables.texts)

        if f:
            try:
                return f.format(**d)
            except Exception as e:
                print(e)
                return 'Format error for %s' % e