import threading


def create_thread(func, *args, **kwargs):
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()


def run_thread(func):
    def f(*args, **kwargs):
        create_thread(func, *args, **kwargs)
    return f
