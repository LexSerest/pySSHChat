from pysshchat.lib import keycode as keys
from ..commands import handler, keypress_handler
import logging
logging = logging.getLogger('keypress')


def keypress(user, byte):
    if byte in keys.KEY_ENTER:
        if user.text[:1] == '/':
            try:
                args = user.text[1:].split(' ')
                handler(user, args[0], args[1:])
                user.text = ''
                #user.reset_input()
            except Exception as e:
                logging.exception(user.text, e)
        else:
            if user.text.strip():
                user.send()
    if byte in keys.KEY_CTRL_D:
        user.close()

    try:
        keypress_handler(user, byte)
    except Exception as e:
        logging.exception(e)
