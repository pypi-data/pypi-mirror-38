# -*- coding: utf-8 -*-

from contextlib import contextmanager
import os
import tempfile


def _tempfile(filename):
    """
    Create a NamedTemporaryFile instance to be passed to atomic_writer
    """
    return tempfile.NamedTemporaryFile(mode='w',
                                       dir=os.path.dirname(filename),
                                       prefix=os.path.basename(filename),
                                       suffix='.tmp',
                                       delete=False)


@contextmanager
def atomic_write(filename):
    """
    Open a NamedTemoraryFile handle in a context manager
    """
    f = _tempfile(filename)

    try:
        yield f

    finally:
        f.close()
        # replace the original file with the new temp file (atomic on success)
        os.replace(f.name, filename)
