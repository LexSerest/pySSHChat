import urwid
import logging

from pysshchat.user import UserBase
from pysshchat.user.ui.screen import AsyncScreen
from pysshchat.user.ui.alert import Alert
from pysshchat.user.ui.chat import Chat
from pysshchat.user.ui.palette import palette
from pysshchat.libs import run_thread


from pysshchat.store import store
users = store.users

logging = logging.getLogger("pysshchat.user.ui")


class UI(UserBase):
    message = None
    output = None
    body = None
    list = None
    header = None
    input = None
    footer = None
    context = None
    screen = None

    def __init__(self, username, process, loop):
        super().__init__(username, process, loop)
        self.screen = AsyncScreen(process)
        self.run(self.screen, loop)
        self.load_history()

    def build_interface(self):
        self.header = urwid.Text(self.title.strip())
        self.input = urwid.Edit(self.text_format("format.prompt", u=self))

        self.message = urwid.AttrWrap(urwid.Text(""), "msg_info") #Alert()

        self.output = urwid.SimpleListWalker([])
        self.body = Chat(self.output)
        list_user = [urwid.Text(u) for u in users.keys()]
        self.list = urwid.ListBox(urwid.SimpleListWalker(list_user))

        w = urwid.Columns([self.body, (12, urwid.AttrWrap(self.list, "list"))], 1)
        self.header = urwid.AttrWrap(self.header, "divider")
        self.footer = urwid.AttrWrap(self.input, "footer")
        w = urwid.AttrWrap(w, "body")
        self.footer.set_wrap_mode("space")
        main_frame = urwid.Frame(w, header=self.header, footer=self.message)
        self.context = urwid.Frame(main_frame, footer=self.footer)
        self.context.set_focus("footer")

    def update_user_list(self):
        list_user = [urwid.Text((name)) for name in users]
        self.list._set_body(urwid.SimpleListWalker(list_user))

    def exit(self):
        if hasattr(self.main_loop, "idle_handle"):
            try:
                self.main_loop.stop()
            except BrokenPipeError:
                pass
        super().exit()

    def event_join_another(self):
        self.update_user_list()

    def event_quit_another(self):
        self.update_user_list()

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

    def message_print(self, type, **kwargs):
        text = self.text_format(type, **kwargs)
        walker = self.output
        walker[:] = walker[-100:]
        walker.append(urwid.Text(text))
        self.body.scroll_to_bottom()
        return text

    def keypress(self, size, key):
        urwid.emit_signal(self, "keypress", size, key)

        if key in ("page up", "page down"):
            self.body.keypress(size, key)

        elif key in ("down", "up"):
            self.body.scroll(key)

        elif key in ("ctrl d", "ctrl c"):
            self.exit()

        elif key == "tab":
            text = self.input.get_edit_text()
            try:
                self.event_key_tab(text)
            except Exception as e:
                logging.exception(e)

        elif key == "ctrl w":
            self.input.set_edit_text("")

        elif key == "enter":
            text = self.input.get_edit_text()
            self.input.set_edit_text("")

            if text.strip():
                self.event_key_enter(text)

        else:
            self.event_key(key)

    def text_format(self, key, **kwargs):
        out = []

        texts = super().text_format(key, **kwargs)
        out.append(("default", texts[0]))

        colors = texts[1::2]
        for index, text in enumerate(texts[2::2]):
            color = colors[index]
            if text:
                if color == "-":
                    out.append(("default", text))
                elif color == "b":
                    out.append(("bold", text))
                elif color == "i":
                    out.append(("italics", text))
                elif color == "u":
                    out.append(("underline", text))
                elif color == "info":
                    out.append(("info", text))
                else:
                    out.append(("h" + color, text))

        return out

    def change_color(self, color=False):
        super().change_color(color)
        self.input.set_caption(self.text_format("format.prompt", u=self))

    def event_key_tab(self, text):
        if not len(text):
            return

        args = text.split(" ")
        text = args[-1]
        keys = store.users.keys()

        if text[0] == "/":
            keys = store.get_commands_list(self.is_admin)
            text = text[1:]

        #l = self.input.edit_pos
        #self.input.set_edit_text(self.footer.edit_text[:l])
        users_find = [u for u in keys if u.startswith(text)]
        if len(users_find):
            self.input.insert_text(users_find[0][len(text):])
            #self.input.set_edit_pos(l)
