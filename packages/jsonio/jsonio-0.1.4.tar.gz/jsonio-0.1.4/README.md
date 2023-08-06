
[![CircleCI](https://circleci.com/gh/ylathouris/jsonio.svg?style=shield)](https://circleci.com/gh/ylathouris/jsonio)  ![Coverage](coverage.svg)

---

# jsonio

The `jsonio` package provides utility functions for reading and writing JSON data. It supports the following features:

* [Easy Read/Write](#readwrite)
* [Works Just Like The `json` Library](#json)
* [Supports `datetime/date` Objects](#datetime)
* [Supports `dataclasses` (Python 3.7+)](#dataclass)
* [Preserve Ordering](#ordereddict)

</br>

## Installation

```
pip install jsonio
```

</br>

### <a name="readwrite"></a>Easy Read/Write

**Read**

```python
import jsonio

data = jsonio.read('/foo/bar.json')
```

**Write**

```python
import jsonio

jsonio.write({'foo': 'bar'}, '/foo/bar.json')
```

</br>


### <a name="json"></a>Works Just Like The `json` Library

**Load**

```python
import jsonio

with open('/foo/bar.json', 'r') as jsonfile:
    data = jsonio.load(jsonfile)
```

**Loads**

```python
import jsonio

data = jsonio.loads('{"foo": "bar"}')
```

**Dump**

```python
import jsonio

with open('/foo/bar.json', 'w') as jsonfile:
    jsonio.dump({'foo': 'bar'}, jsonfile)
```

**Dumps**

```python
import jsonio

data = {
    'apple': 'crumble',
    'banana': 'split',
}

# Use standard options.
text = jsonio.dumps(data, jsonfile, indent=2, sort_keys=True)
```

</br>


### <a name="datetime"></a>Supports `date/datetime` Objects


```python
import datetime
import jsonio

before = {
    'date': datetime.date.today(),
    'timestamp': datetime.datetime.now(),
}

data = jsonio.dumps(before)
after = jsonio.loads(data)
assert before == after  # True
```

</br>


### <a name="dataclasses"></a>Supports `dataclasses` (Python 3.7+)

```python
from dataclasses import dataclass
import jsonio


@dataclass
class Fruit:
    apple: str
    banana: str


before = Fruit(apple='Fuji', banana='Lady Finger')

data = jsonio.dumps(before)
after = jsonio.loads(data)
assert before == after  # True
```

</br>

### <a name="ordereddict"></a>Preserve Ordering - i.e. `OrderedDict` Objects

```python
import collections
import jsonio

before = collections.OrderedDict([('banana', 'split'), ('apple', 'crumble')])

text = jsonio.dumps(before, indent=2)
after = jsonio.loads(text, ordered=True)
assert before == after  # True
```
