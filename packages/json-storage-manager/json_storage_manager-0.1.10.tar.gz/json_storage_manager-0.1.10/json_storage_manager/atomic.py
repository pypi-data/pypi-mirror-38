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
    f = _tempfile(os.fsencode(filename))

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
    with open(os.fsencode(str(filename)), "r") as f:
        data = json.load(f)
        results = [i for i in data if i["uuid"] == str(uuid)]
        if results:
            return results
        return None


def set_item(filename, item):
    """
    Save entry to JSON file
    """
    with atomic_write(os.fsencode(str(filename))) as temp_file:
        with open(os.fsencode(str(filename))) as products_file:
            # load the JSON data into memory
            products_data = json.load(products_file)
        # check if UUID already exists
        uuid_list = [i for i in filter(
            lambda z: z["uuid"] == str(item["uuid"]), products_data)]
        if len(uuid_list) == 0:
            # add the new item to the JSON file
            products_data.append(item)
            # save the new JSON to the temp file
            json.dump(products_data, temp_file)
            return True
        return None  # record already exists


def update_item(filename, item, uuid):
    """
    Update entry by UUID in the JSON file
    """
    with atomic_write(os.fsencode(str(filename))) as temp_file:
        with open(os.fsencode(str(filename))) as products_file:
            # load the JSON data into memory
            products_data = json.load(products_file)
        # apply modifications to the JSON data wrt UUID
        [products_data[i].update(item) for (
            i, j) in enumerate(products_data) if j["uuid"] == str(uuid)]
        # save the modified JSON data into the temp file
        json.dump(products_data, temp_file)
        return True
