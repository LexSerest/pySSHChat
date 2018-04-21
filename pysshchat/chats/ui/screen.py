import asyncio
import urwid
from urwid.raw_display import Screen
from contextlib import suppress

class AsyncScreen(Screen):
    def __init__(self, transport):
        self.transport = transport
        self.reader = transport.stdin
        self.writer = transport.stdout

        Screen.__init__(self)
    _pending_task = None


    def get_cols_rows(self):
        width, height, pixwidth, pixheight = self.transport.get_terminal_size()
        return width, height

    def write(self, data):
        self.writer.write(data)

    def flush(self):
        pass

    def hook_event_loop(self, event_loop, callback):
        def pump_reader(fut=None):
            if fut is None:
                # First call, do nothing
                pass
            elif fut.cancelled():
                # This is in response to an earlier .read() call, so don't
                # schedule another one!
                return
            elif fut.exception():
                callback(['window resize'], [])
            else:
                try:
                    co = bytearray(fut.result(), 'utf-8')
                    self.parse_input(event_loop, callback, co)

                except urwid.ExitMainLoop:
                    self.writer.abort()
                except:
                    return

            self._pending_task = asyncio.ensure_future(
                self.reader.read(1024), loop=event_loop._loop)
            self._pending_task.add_done_callback(pump_reader)

        pump_reader()


    def unhook_event_loop(self, event_loop):
        if self._pending_task:
            self._pending_task.cancel()
            del self._pending_task
