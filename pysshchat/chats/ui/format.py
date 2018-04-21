import re
import logging
from functools import reduce
import pysshchat.variables as var
logging = logging.getLogger('format')


def dotget(key):
    try:
        return reduce(lambda c, k: c[k], key.split('.'), var.texts)
    except:
        print('Not found texts.yaml key %s' % key)
        return ''


def text_format(key, **kwargs):
    text = dotget(key).format(**kwargs)
    pattern = r'(.*?)\(#(.*?)#(.*?)#\)(.*)'
    find = re.findall(pattern, text, re.DOTALL)

    if not len(find):
        return text

    out = []
    for el in find:
        left, type, text, rigth = el
        arr = []
        if left:
            arr.append(('default', left))
        if text:
            arr.append((type, text))
        if rigth:
            arr.append(('default', rigth))
        out.extend(arr)
    return out
