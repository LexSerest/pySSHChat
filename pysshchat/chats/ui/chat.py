import urwid


class Chat(urwid.ListBox):
    def __init__(self, body):
        super().__init__(body)
        self.body = body
        urwid.emit_signal(self, "set_auto_scroll", True)

    def keypress(self, size, key):
        urwid.ListBox.keypress(self, size, key)

    def scroll_to_bottom(self):
        if len(self.body):
            self.set_focus(len(self.body) - 1)

    def scroll(self, type):
        if type == "down":
            self.focus_next()
        if type == "up":
            self.focus_previous()

    def focus_next(self):
        try:
            self.body.set_focus(self.body.get_next(self.body.get_focus()[1])[1])
        except:
            pass

    def focus_previous(self):
        try:
            self.body.set_focus(self.body.get_prev(self.body.get_focus()[1])[1])
        except:
            pass