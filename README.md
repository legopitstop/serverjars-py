# serverjars-api

![Tests](https://github.com/legopitstop/serverjars-py/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/serverjars-api)](https://pypi.org/project/serverjars-api/)
[![Python](https://img.shields.io/pypi/pyversions/serverjars-api)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/serverjars-api)
![Status](https://img.shields.io/pypi/status/serverjars-api)
[![Issues](https://img.shields.io/github/issues/legopitstop/serverjars-py)](https://github.com/legopitstop/serverjars-py/issues)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Download and fetch details about Minecraft server jars.

## Installation
Install the module with pip:
```bat
pip3 install serverjars-api
```
Update existing installation: `pip3 install serverjars-api --upgrade`

## Features

- Access vanilla or modded Minecraft jars. 
- No 3rd party APIs. 
- Add support for your own jar service. 

## Links

- [Documentation](https://docs.lpsmods.dev/serverjars-api)
- [Source Code](https://github.com/legopitstop/serverjars-py)

## Dependencies

| Name                                           | Description                                      |
| ---------------------------------------------- | ------------------------------------------------ |
| [requests](https://pypi.org/project/requests/) | Requests is a simple, yet elegant, HTTP library. |
| [pydantic](https://pypi.org/project/pydantic/) | Data validation using Python type hints          |

## Code Examples:
Fetching the latest jar:
```python
import serverjars
latest = serverjars.fetch_latest('vanilla', 'release')
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

serverjars.download_jar('vanilla', "release")
```

Create and run a Minecraft server
```python
import serverjars

app = serverjars.App.create('vanilla', "release", fp="svr/server.jar")
app.run()
```
