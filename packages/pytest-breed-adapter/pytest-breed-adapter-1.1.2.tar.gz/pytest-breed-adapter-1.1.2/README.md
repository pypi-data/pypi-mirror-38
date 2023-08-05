# pytest-breed-adapter

A simple plugin generate json report and sent to breed server for report visualization

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.

Installation
------------
You can install "pytest-breed-adapter" via `pip`_ from `PyPI`_::

    $ pip install pytest-breed-adapter


Usage
-----
For full functionality you need build `breed-server` which is close-source project
But you can build your own server for further usage, plugin will send json report to
breed server address + `/report/parse`

```
[pytest]
addopts              = --breed
json_report_file     = auto/ none/ arbitary.json
json_report_indent   = 4/ none
metadata             = true/ false
CI_server            = 192.168.1.199
breed_server         = http://192.168.1.199:62180
```

```
test_demo():
    """
    @ Node id
    @! key0: value0
    @! key1: value1
    @! key2: value2
    @! key3: value3
    """
    assert 1
```
first line of docstring startswith @`space` will be parsed to test nodeid
reset line with `@!` prefix will be treated as metadata key-value

Contributing
------------
Contributions are very welcome

License
-------

Distributed under the terms of the `BSD-3`_ license, "pytest-breed-adapter" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.
