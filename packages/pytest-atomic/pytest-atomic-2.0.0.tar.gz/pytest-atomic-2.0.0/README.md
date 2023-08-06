# Welcome to pytest-atomic
[![PyPi version](https://img.shields.io/pypi/v/pytest-atomic.svg)](https://pypi.org/project/pytest-atomic/)
![Python version](https://img.shields.io/pypi/pyversions/pytest-atomic.svg)
[![Build Status](https://travis-ci.com/megachweng/pytest-atomic.svg?branch=master)](https://travis-ci.com/megachweng/pytest-atomic)
[![codecov](https://codecov.io/gh/megachweng/pytest-atomic/branch/master/graph/badge.svg)](https://codecov.io/gh/megachweng/pytest-atomic)  

Skip rest of tests if previous test failed.

## Requirements
* pytest >= 3.10.0
* python >= 3.6

**Not compatible with Python2.x**

## How to install
`$ pip install pytest-atomic --upgrade`

## Usage
```ini
# pytest.ini
[pytest]
[atomic]
enable     : true
electronic : true
```
## Options
>**Notice!** [pytest]section must be included.  
>**Notice!** All options bellow must be under [atomic] section in pytest.ini.
* enable     : [true / false] default is false
* electronic : [true / false] default is true 
## Example
```python
import pytest

@pytest.mark.atomic
def test_fn1():
    assert 0

def test_fn2():
    assert 0

class TestCls:
    @pytest.mark.atomic
    def test_1(self):
        assert 0
    @pytest.mark.electronic
    def test_2(self):
        assert 1
    def test_3(self):
        assert 0
    @pytest.mark.electronic
    def test_4(self):
        assert 1
    def test_5(self):
        assert 0

def test_fn3():
    assert 0
@pytest.mark.atomic
def test_fn4():
    assert 0
def test_fn5():
    assert 0
```

```text
test_demo
|____ test_fn1: Failed
|____ test_fn2: Skipped
|____ TestCls
|   |____ test_1 Failed
|   |____ test_2 Passed
|   |____ test_3 Skipped
|   |____ test_4 Passed
|   |____ test_5 Skipped
|
|____ test_fn3: Skipped
|____ test_fn4: Failed
|____ test_fn5: Skipped   
```

## Contributing
Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/), please ensure
the coverage at least stays the same before you submit a pull request.

## License
Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license, "pytest-atomic" is free and open source software


## Known Issue
* Mark a Test class directly seems not work, but you can mark the first of test method in that class.  