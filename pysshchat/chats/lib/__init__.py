import _thread as thread
from functools import reduce
import logging
logging = logging.getLogger('lib')


def run_thread(func):
    def f(*args):
        return thread.start_new_thread(func, args)
    return f


def dotget(key, cfg):
    try:
        return reduce(lambda c, k: c[k], key.split('.'), cfg)
    except Exception as e:
        logging.exception(e)
        return ''
