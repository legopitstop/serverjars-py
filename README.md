# serverjars
The unofficial Python wrapper for [serverjars.com](https://serverjars.com/)

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
