import urwid
import logging

import pysshchat.variables as variables
from pysshchat.chats.ui import UI
from pysshchat.chats.ui.screen import AsyncScreen
from .commands import handler, keypress_handler

logging = logging.getLogger('user_ui')


class UserUI(UI):
    def __init__(self, username, process, loop):
        self.process = process
        self.loop = loop

        process.channel.set_echo(False)
        process.stdin.channel.set_line_mode(False)

        super().__init__(username)
        screen = AsyncScreen(process)
        self.run(screen, loop)
        self.event_join()

    def send(self, text, type='format.msg', me=True):
        variables.add_history(self.message_format(type, text=text))
        for username, user in variables.users.items():
            if not me and user == self:
                continue
            user.print_message(type, text=text, u=self)


    def local(self, type, **kwargs):
        self.print_message(type, **kwargs)

    async def exit(self):
        try:
            self.quit(False)
            self.process.close()
            await self.process.wait_closed()
        except Exception as e:
            print(e)
            pass

    async def wait_close(self):
        await self.process.wait_closed()

    def event_key(self, key):
        keypress_handler(self, key)

    def event_join(self):
        self.send('', 'messages.connect')
        variables.users[self.username] = self


        # update user list
        for user in variables.users.values():
            user.set_user_list(variables.users.keys())

        # history load
        for line in variables.history:
            self.output.append(urwid.Text(line))

    def event_quit(self):
        variables.users.pop(self.username)
        self.process.close()
        #self.loop.run_until_complete(self.wait_close)

        self.send('', 'messages.disconnect', False)

        for user in variables.users.values():
            user.set_user_list(variables.users.keys())

    def event_key_enter(self, text):
        try:
            if text[0] == '/':
                cmd = text[1:].split(' ')
                handler(self, cmd[0], cmd[1:])
            else:
                self.send(text)
        except Exception as e:
            logging.exception(e)

    def event_key_tab(self, text):
        pass

