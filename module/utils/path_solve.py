import sys
from os.path import abspath, join


def get_resource_path(relative_path) -> str:
    if hasattr(sys, '_MEIPASS'):
        return join(sys._MEIPASS, relative_path)
    return join(abspath("."), relative_path)
