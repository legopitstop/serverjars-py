# ServerJars-API
The unofficial Python API for ServerJars

**Code Examples:**

**Fetching the latest jar:**
```python
latest = ServerJars.fetchLatest(category=Category.vanilla)
print(latest)
```

**Fetching all the Jars:**
```python
allJars = ServerJars.fetchAll(category=Category.paper)
print(allJars)
```

**Fetching types:**
```python
types = ServerJars.fetchTypes()
print(types)
```

**Fetching subtypes:**
```python
subtypes = Serverjars.fetchTypes(type=Type.bedrock)
print(subtypes)
```

**Downloading Jars:**
```python
download = ServerJars.downloadJar(type=Category.purpur, version='1.13.2')
print(download)
```

## Jar

The Jar class gets returned from most of the classes in this library.

### Parameters
- `version` - The version of the jar
- `size` - The size of the jar.
- `md5` - md5 of the jar
- `built` - The timestamp of when it was releaseed.
- `stability` - The stability of the jar
