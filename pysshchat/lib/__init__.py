import threading
from functools import reduce
import logging
logging = logging.getLogger('lib')


def run_thread(func):
    def f(*args):
        thread = threading.Thread(target=func, args=args)
        thread.daemon = True
        thread.start()
    return f


def dotget(key, cfg):
    try:
        return reduce(lambda c, k: c[k], key.split('.'), cfg)
    except Exception as e:
        logging.exception(e)
        return ''
