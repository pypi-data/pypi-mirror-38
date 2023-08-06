# Welcome to pytest-informative-node
![PyPi version][pypi] ![Python version][python version] ![code coverage][coverage]
[![Build Status](https://travis-ci.com/megachweng/pytest-informative-node.svg?branch=master)](https://travis-ci.com/megachweng/pytest-informative-node)
[![codecov](https://codecov.io/gh/megachweng/pytest-informative-node/branch/master/graph/badge.svg)](https://codecov.io/gh/megachweng/pytest-informative-node)  
display more node information.

## Requirements
* pytest >= 3.10.0
* python >= 3.6

**Not compatible with Python2.x**

## How to install
`$ pip install pytest-informative-node`
## How to use
```ini
# pytest.ini
[pytest]
[informative_node_id]
enable    : true
delimiter : @
```

write docstring with `leading delimiter` you defined in `pytest.ini [informative_node_id]` section as node name.
```python
class TestClass:
    """@you node id"""

def test_func():
    """@you node id"""
``` 
> Test file and Test Package is also supported, just write docstring in the top of file and `__init__.py` respectively.
## Options
> **Notice!** `[pytest]`section **must** be included.  
> **Notice!** All options bellow **must** be under `[informative_node_id]` section in `pytest.ini`.
* `enable`    : [true / false] default is `false`. 
* `delimiter` : the delimiter to extract node_id in docstring, default is `@`.

## Example
```python
# Test file structure
scenario
|
|__functionality
    |__ __init__.py
    |   |# content of __init__.py
    |   |"""@LoginSection"""
    |   #\---------------------
    |
    |__ test_one.py
        |# content of __init__.py
        |   """@TestFile"""
        |   import pytest
        |   class TestClass:
        |       """@TestGroup"""
        |       
        |       @pytest.mark.parametrize('n', [1, 2], ids=['first', 'second'])
        |       def test_demo(self, n):
        |           """@DemoTest"""
        |           assert n == 1
        #\-----------------------
```
```text
# Test report structure
✕LoginSection
|
|__ ✕TestFile
    |
    |__ ✕TestGroup
        |
        |__ ✕Demo Test
            |__ ✓first
            |__ ✕second

```
## Contributing
Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/), please ensure
the coverage at least stays the same before you submit a pull request.

## License
Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license, "pytest-informative-node" is free and open source software


## Known Issue
* If you test with Pycharm, you cannot navigate back to source test file from Test Runner tab.

[coverage]:https://codecov.io/gh/megachweng/pytest-informative-node/branch/master/graph/badge.svg
[pypi]:https://img.shields.io/pypi/v/pytest-informative-node.svg
[python version]:https://img.shields.io/pypi/pyversions/pytest-informative-node.svg
[ci]:https://travis-ci.com/megachweng/pytest-informative-node.svg?branch=masterravis-ci.org/megachweng/pytest-informative-node.svg?branch=master