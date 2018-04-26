import datetime
import urwid
import random
import logging
from .alert import Alert
from .chat import Chat
from .palette import palette
from .format import text_format

logging = logging.getLogger('ui')


class UI(object):
    def __init__(self, username):
        self.title = text_format('text.title', u=self)
        self.username = username

        self.message = None
        self.output = None
        self.body = None
        self.list = None
        self.header = None
        self.input = None
        self.context = None

        self.color = None
        self.screen = None
        self.main_loop = None
        self.rnd_color()

    def rnd_color(self):
        self.color = 'h' + str(random.randint(1, 254))

    def change_color(self):
        self.rnd_color()
        self.input.set_caption(text_format('format.prompt', u=self))

    def run(self, screen, loop):
        self.screen = screen
        screen.set_terminal_properties(colors=256)
        self.screen.register_palette(palette())
        self.build_interface()

        def input_cb(key):
            self.size = self.screen.get_cols_rows()
            self.keypress(self.size, key)

        self.main_loop = urwid.MainLoop(
            self.context,
            screen=self.screen,
            handle_mouse=False,
            unhandled_input=input_cb,
            event_loop=urwid.AsyncioEventLoop(loop=loop),
        )

        self.main_loop.start()

    def resize(self):
        self.main_loop.screen_size = None

    def quit(self, event=True):
        try:
            urwid.emit_signal(self, "quit")
            if hasattr(self.main_loop, 'idle_handle'):
                self.main_loop.stop()
            if event:
                self.event_quit()
        except Exception as e:
            logging.exception(e)

    def build_interface(self):
        self.header = urwid.Text(self.title)
        self.input = urwid.Edit(text_format('format.prompt', u=self))

        self.message = Alert()

        self.output = urwid.SimpleListWalker([])
        self.body = Chat(self.output)
        list_user = [urwid.Text(u) for u in self.get_user_list()]
        self.list = urwid.ListBox(urwid.SimpleListWalker(list_user))

        w = urwid.Columns([self.body, (12, urwid.AttrWrap(self.list, "list"))], 1)
        self.header = urwid.AttrWrap(self.header, "divider")
        self.input = urwid.AttrWrap(self.input, "footer")
        w = urwid.AttrWrap(w, "body")
        self.input.set_wrap_mode("space")
        main_frame = urwid.Frame(w, header=self.header, footer=self.message)
        self.context = urwid.Frame(main_frame, footer=self.input)
        self.context.set_focus("footer")

    def get_user_list(self):
        return []

    def set_user_list(self, users):
        # users - (username, format)
        #list_user = [urwid.Text((color, name)) for name, color in users]
        list_user = [urwid.Text((name)) for name in users]
        self.list._set_body(urwid.SimpleListWalker(list_user))

    def set_title(self, title):
        self.header.set_text(title)

    def keypress(self, size, key):
        urwid.emit_signal(self, "keypress", size, key)

        if key in ("page up", "page down"):
            self.body.keypress(size, key)

        elif key in ("down", "up"):
            self.body.scroll(key)

        elif key in ("ctrl d", 'ctrl c'):
            self.quit()

        elif key == "tab":
            self.event_key_tab(self.input.get_edit_text())

        elif key == "enter":
            self.key_enter()

        else:
            self.event_key(key)
            self.context.keypress(size, key)

    def message_format(self, type, **kwargs):
        kwargs['time'] = self.get_time()
        if not kwargs.get('u', None):
            kwargs['u'] = self
        return text_format(type, **kwargs)

    def print_message(self, type, **kwargs):
        walker = self.output
        text = self.message_format(type, **kwargs)
        walker.append(urwid.Text(text))
        self.body.scroll_to_bottom()
        return text

    def print_text(self, text):
        walker = self.output
        if not isinstance(text, urwid.Text):
            text = urwid.Text(text)         # color for nick?
        walker.append(text)
        self.body.scroll_to_bottom()

    def get_time(self):
        return datetime.datetime.now().strftime('%H:%M')

    def key_enter(self):
        text = self.input.get_edit_text()

        self.input.set_edit_text(" " * len(text))
        self.input.set_edit_text("")

        if text.strip():
            self.event_key_enter(text)

    def alert(self, type, text, delay=3):
        self.message.set_temp(type, text, delay)

    def event_key_enter(self, text):
        pass

    def event_quit(self):
        pass

    def event_key(self, key):
        pass

    def event_key_tab(self, text):
        # self.divider.set_temp('danger', str(self.ui.get_cols_rows()))
        # l = self.footer.edit_pos
        # self.footer.set_edit_text(self.footer.edit_text[:l])
        # self.footer.insert_text(str(self.zzz))
        # self.zzz += 1
        # self.footer.set_edit_pos(l)
        pass

