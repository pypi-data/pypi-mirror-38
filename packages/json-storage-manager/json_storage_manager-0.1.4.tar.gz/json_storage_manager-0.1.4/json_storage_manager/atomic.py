# -*- coding: utf-8 -*-

from contextlib import contextmanager
import os
import tempfile
import json


def _tempfile(filename):
    """
    Create a NamedTemporaryFile instance to be passed to atomic_writer
    """
    return tempfile.NamedTemporaryFile(mode='w',
                                       dir=os.path.dirname(filename),
                                       prefix=os.path.basename(filename),
                                       suffix=os.fsencode('.tmp'),
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


def get_item(filename, uuid):
    """
    Read entry from JSON file
    """
    with open(filename, "r") as f:
        data = json.load(f)
        results = [i for i in data if i["uuid"] == str(uuid)]
        if results:
            return results
        return None


def set_item(filename, item):
    """
    Save entry to JSON file
    """
    with atomic_write(filename) as temp_file:
        with open(filename) as products_file:
            # get the JSON data into memory
            products_data = json.load(products_file)
        # now process the JSON data
        products_data.append(item)
        # save the modified JSON data into the temp file
        json.dump(products_data, temp_file)
        return True
