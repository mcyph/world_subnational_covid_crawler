# https://stackoverflow.com/questions/18593661/how-do-i-strftime-a-date-object-in-a-different-locale
import locale
import threading
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()


@contextmanager
def set_locale(name):
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

