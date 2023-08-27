# serverjars-api

[![PyPI](https://img.shields.io/pypi/v/serverjars-api)](https://pypi.org/project/serverjars-api/)
[![Python](https://img.shields.io/pypi/pyversions/serverjars-api)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/serverjars-api)
![Status](https://img.shields.io/pypi/status/serverjars-api)
[![Issues](https://img.shields.io/github/issues/legopitstop/serverjars-python-api-wrapper)](https://github.com/legopitstop/serverjars-python-api-wrapper/issues)

The unofficial Python wrapper for [serverjars.com](https://serverjars.com/)

## Installation
Install the module with pip:
```bat
pip3 install serverjars-api
```
Update existing installation: `pip3 install serverjars-api --upgrade`

## Code Examples:
Fetching the latest jar:
```python
import serverjars
latest = serverjars.fetchLatest('vanilla')
print(latest)
```

Fetching all the Jars:
```python
import serverjars
allJars = serverjars.fetchAll('paper')
print(allJars)
```

Fetching types:
```python
import serverjars
types = serverjars.fetchTypes()
print(types)
```

Fetching subtypes:
```python
import serverjars
subtypes = serverjars.fetchTypes('bedrock')
print(subtypes)
```

Downloading Jars:
```python
import serverjars

def on_finish(jar):
    print('Downloaded', jar)

serverjars.downloadJar('snapshot', finishcommand=on_finish)
```
