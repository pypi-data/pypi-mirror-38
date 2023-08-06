# AIConf
This project provides convenience functions to handle config files in HOCON, in particular for the selection of the use of implemented classes and their parameter orchestration.

## Installation
```bash
git clone git@gitlab.com:semanchester/aisample.git
cd aisample
pip install .
```
for tests, run
```bash
pip install requirements-dev.txt
python setup.py test
```

to build the documentation, run
```bash
python setup.py build_sphinx
```

## Example

Say you have multiple implementations of `SomeInterface`
```python
class SomeInterface:
    ...

class SomeClass(SomeInterface):
    def __init__(self, arg1, arg2):
        ...
class SomeOtherClass(SomeInterface):
    def __init__(self, arg3, arg4):
        ...
```
You want to use a config file `sample.conf` to select appropriate implementations transparently and choose appropriate parameters.
```hocon
impl_1 = {
  '()' = somepackage.SomeClass
  arg1 = 3
  arg2 = 4
}
impl_2 = {
  '()': somepackage.SomeOtherClass
  arg3 = true
  arg4 = false
}
```
calling
```python
from aiconf import ConfigReader
from aiconf import construct_from_config
cfg = ConfigReader('sample.conf').read_config()
impl_1 = construct_from_config(cfg['impl_1'])
impl_2 = construct_from_config(cfg['impl_2'])

assert isinstance(impl_1, SomeClass)

assert isinstance(impl_1, SomeOtherClass)
```

For further information, refer to the documentation.