# -*- coding: utf-8 -*-

from pathlib import Path


def is_file(filename):
    my_file = Path(filename)
    if my_file.is_file():
        # file exists
        return True
    return None
