[![Build Status](https://travis-ci.org/hefnawi/json-storage-manager.svg?branch=master)](https://travis-ci.org/hefnawi/json-storage-manager) [![License](https://img.shields.io/pypi/l/json-storage-manager.svg)](https://pypi.org/project/json-storage-manager) [![PyPI version](https://badge.fury.io/py/json-storage-manager.svg)](https://badge.fury.io/py/json-storage-manager) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/08b84b770a7245a9b4cf613c4eb7b857)](https://www.codacy.com/app/hefnawi/json-storage-manager?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hefnawi/json-storage-manager&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/08b84b770a7245a9b4cf613c4eb7b857)](https://www.codacy.com/app/hefnawi/json-storage-manager?utm_source=github.com&utm_medium=referral&utm_content=hefnawi/json-storage-manager&utm_campaign=Badge_Coverage) [![Documentation Status](https://readthedocs.org/projects/json-storage-manager/badge/?version=latest)](https://json-storage-manager.readthedocs.io/en/latest/?badge=latest)

# json-storage-manager
`json-storage-manager` is a Python Package that simply manages the JSON files with the stored data of products and orders for a demo store API.

## Installation
```bash
pip install json-storage-manager
```

## atomic

### Usage
`atomic` is basically used as a custom context manager for writing JSON files without downtime for the original file.
It simply loads the JSON file into memory and opens a temporary file using the `tempfile` Python Package, finally once the operation is finished it performs an  `os.replace()` to replace the original file (which is an atomic operation on Linux systems).

```python
from json_storage_manager import atomic

with atomic.atomic_write(str(json_file)) as temp_file:
        with open(str(json_file)) as products_file:
            # get the JSON data into memory
            products_data = json.load(products_file)
        # now process the JSON data
        products_data.append(
            {'uuid': "2299d69e-deba-11e8-bded-680715cce955",
             'special_price': 111.0,
             'name': "Test Product"
             })
        json.dump(products_data, temp_file)
```
