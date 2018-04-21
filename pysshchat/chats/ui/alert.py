import urwid
import threading
import time


def run_thread(func):
    def f(*args):
        thread = threading.Thread(target=func, args=args)
        thread.daemon = True
        thread.start()
    return f


class Alert(urwid.AttrWrap):
    def __init__(self, text=""):
        self.text = urwid.Text(text)
        super().__init__(self.text, "msg_info")

    @run_thread
    def default(self, delay):
        time.sleep(delay)
        self.text.set_text("")
        self.set_attr("msg_info")

    def set_temp(self, type, text, delay=3):
        self.text.set_text(text)
        self.set_attr("msg_" + type)
        self.default(delay)