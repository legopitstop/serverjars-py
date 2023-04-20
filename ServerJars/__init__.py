from .constants import *
import requests
import os
import threading

__version__ = '1.1.0'
__all__ = [
    'downloadJar', 'fetchLatest', 'fetchAll', 'fetchTypes', 'fetchDetails'
]


class InvalidRequest(Exception):
    pass


class JarNotFoundError(Exception):
    pass


class Size():
    def __init__(self, display=None, bytes=None):
        self.display: str = display
        self.bytes: int = bytes

    def __str__(self):
        return self.display

    def json(self):
        return {
            'display': self.display,
            'bytes': self.bytes
        }

    def from_json(self, data: dict):
        if 'display' in data:
            self.display = data['display']
        if 'bytes' in data:
            self.bytes = data['bytes']
        return self


class Jar():
    def __init__(self, version: str = None, file: str = None, size: Size = None, md5: str = None, built: int = None, stability: str = None):
        self.version: str = version
        self.file: str = file
        self.size: Size = size
        self.md5: str = md5
        self.built: int = built
        self.stability: str = stability

    def __str__(self):
        return f"Jar(version='{self.version}', file='{self.file}', size='{self.size}')"

    def json(self):
        return {
            'version': self.version,
            'file': self.file,
            'size': self.size.json(),
            'md5': self.md5,
            'built': self.built,
            'stability': self.stability
        }

    def from_json(self, data: dict):
        if 'version' in data:
            self.version = data['version']
        if 'file' in data:
            self.file = data['file']
        if 'size' in data:
            self.size = Size().from_json(data['size'])
        if 'md5' in data:
            self.md5 = data['md5']
        if 'built' in data:
            self.built = data['built']
        if 'stability' in data:
            self.stability = data['stability']
        return self


def _type(category: str):
    dat = sendRequest('fetchTypes')
    for type in dat:
        for cat in dat[type]:
            if cat == category:
                return type
    return None


def sendRequest(*args: str):
    endpoint = ''
    for arg in args:
        if arg is not None:
            endpoint += str(arg)+'/'
    url = 'https://serverjars.com/api/'+endpoint
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return data.get('response')
    elif res.status_code == 404:
        raise JarNotFoundError(f'Jar not found! {url}')
    raise InvalidRequest(f'{res.status_code} Try again!')


def downloadJar(category: str, file: str = None, version: str = None, thread: bool = False, finishcommand=None) -> None:
    """
    Fetch a direct download link to a specific jar type with either the latest version or a specified one.

    Arguments
    ---
    `category` - The category of jars (spigot, bukkit, paper, etc..)

    `version` - The version of the jar (don't provide for latest)

    `thread` - Download this jar on a seperate thread.
    """
    def download(category, file, version, callback):
        type = _type(category)
        details: Jar = fetchDetails(category, version)
        if file is None:
            file = os.path.join(os.getcwd(), details.file)
        res = requests.get(
            f'https://serverjars.com/api/fetchJar/{type}/{category}/{version}')
        with open(file, 'wb') as jar:
            jar.write(res.content)
        if callback:
            callback(details)

    if version is None:
        version = ''
    if thread:
        t = threading.Thread(target=download, args=[
                             category, file, version, finishcommand])
        t.start()
    else:
        download(category, file, version, finishcommand)


def fetchLatest(category: str) -> Jar:
    """
    Fetch details on the latest jar for a type

    Arguments
    ---
    `category` - The category of jars (spigot, bukkit, paper, etc..)

    """
    type = _type(category)
    res = sendRequest(f'fetchLatest/{type}/{category}')
    return Jar().from_json(res)


def fetchAll(category: str, max: int = 5) -> list[Jar]:
    """
    Fetch details on the all the jars for a type

    Arguments
    ---
    `category` - The category of jars (spigot, bukkit, paper, etc..)

    `max` - The maximum amount of results to respond with. (Default: 5)
    """
    type = _type(category)
    res = sendRequest('fetchAll', type, category, max)
    jars = []
    for i in res:
        jars.append(Jar().from_json(i))
    return jars


def fetchTypes(type: str = None) -> list[str]:
    """
    Fetch a list of the possible jar types.

    Arguments
    ---
    `type` - The type of jars (bedrock, proxies, servers, etc...). Leave empty to see the list of all types
    """
    res = sendRequest('fetchTypes', type)
    if type is None:
        l = []
        for k in res:
            l.append(k)
        return l
    else:
        return res[str(type)]


def fetchDetails(category: str, version: str = None) -> Jar:
    """
    Fetch the details of a single jar.

    Arguments
    ---
    `category` - The type of jars (servers, proxies, modded, etc..)

    `version` - The version of the jar (don't provide for latest)
    """
    type = _type(category)
    res = sendRequest('fetchDetails', type, category, version)
    return Jar().from_json(res)
