# serverjars-api

[![PyPI](https://img.shields.io/pypi/v/serverjars-api)](https://pypi.org/project/serverjars-api/)
[![Python](https://img.shields.io/pypi/pyversions/serverjars-api)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/serverjars-api)
![Status](https://img.shields.io/pypi/status/serverjars-api)
[![Issues](https://img.shields.io/github/issues/legopitstop/serverjars-python-api-wrapper)](https://github.com/legopitstop/serverjars-python-api-wrapper/issues)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

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
latest = serverjars.fetch_latest('vanilla', 'vanilla')
print(latest)
```

Fetching all the Jars:
```python
import serverjars
allJars = serverjars.fetch_all('vanilla', 'snapshot')
print(allJars)
```

Fetching types:
```python
import serverjars
subtypes = serverjars.fetch_types('modded')
print(subtypes)
```

Downloading Jars:
```python
import serverjars

serverjars.download_jar('vanilla', "vanilla")
```

Create and run a Minecraft server
```python
import serverjars

app = serverjars.App.create('vanilla', "vanilla", fp="svr/server.jar")
app.run()
```
