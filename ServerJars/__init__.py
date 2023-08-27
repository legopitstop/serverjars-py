import requests
import os
import threading
import datetime

from .constants import *

__version__ = '1.2.0'
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

    def __int__(self) -> int:
        return self.bytes

    def __eq__(self, other) -> bool:
        if isinstance(other, (Size, int)):
            return int(self) == int(other)
        return False

    def __lt__(self, other) -> bool:
        if isinstance(other, (Size, int)):
            return int(self) < int(other)
        return False

    def __gt__(self, other) -> bool:
        if isinstance(other, (Size, int)):
            return int(self) > int(other)
        return False

    def __le__(self, other) -> bool:
        if isinstance(other, (Size, int)):
            return int(self) <= int(other)
        return False

    def __ge__(self, other) -> bool:
        if isinstance(other, (Size, int)):
            return int(self) >= int(other)
        return False

    @property
    def __dict__(self):
        return {
            'display': self.display,
            'bytes': self.bytes
        }

    @property
    def display(self) -> str:
        return getattr(self, '_display', '0.0 MB')

    @display.setter
    def display(self, value: str | None):
        if value is None:
            setattr(self, '_display', None)
        else:
            setattr(self, '_display', str(value))

    @property
    def bytes(self) -> int:
        return getattr(self, '_bytes', 0)

    @bytes.setter
    def bytes(self, value: int | None):
        if value is None:
            setattr(self, '_bytes', None)
        elif isinstance(value, int):
            setattr(self, '_bytes', value)
        else:
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead")

    @classmethod
    def from_json(cls, data: dict):
        self = cls.__new__(cls)
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
        inner = ', '.join([f'{k}={v!r}' for k, v in self.__dict__.items()])
        return f"Jar({inner})"

    def __eq__(self, other):
        if isinstance(self, Jar):
            return self.version == other.version and self.file == other.file and self.size == other.size and self.md5 == other.md5 and self.built == other.built and self.stability == other.stability
        return False

    @property
    def __dict__(self):
        return {
            'version': self.version,
            'file': self.file,
            'size': self.size.__dict__,
            'md5': self.md5,
            'built': self.built,
            'stability': self.stability
        }

    @property
    def version(self) -> str | None:
        return getattr(self, '_version', None)

    @version.setter
    def version(self, value: str | None):
        if value is None:
            setattr(self, '_version', None)
        else:
            setattr(self, '_version', str(value))

    @property
    def file(self) -> str | None:
        return getattr(self, '_file', None)

    @file.setter
    def file(self, value: str | None):
        if value is None:
            setattr(self, '_file', None)
        else:
            setattr(self, '_file', str(value))

    @property
    def size(self) -> Size:
        return getattr(self, '_size', Size())

    @size.setter
    def size(self, value: Size | None):
        if value is None:
            setattr(self, '_size', Size())
        elif isinstance(value, Size):
            setattr(self, '_size', value)
        else:
            raise TypeError(
                f"Expected Size or None but got '{value.__class__.__name__}' instead")

    @property
    def md5(self) -> str | None:
        return getattr(self, '_md5', None)

    @md5.setter
    def md5(self, value: str | None):
        if value is None:
            setattr(self, '_md5', None)
        else:
            setattr(self, '_md5', str(value))

    @property
    def built(self) -> datetime.datetime | None:
        return getattr(self, '_built', None)

    @built.setter
    def built(self, value: datetime.datetime | None):
        if value is None:
            setattr(self, '_built', None)
        elif isinstance(value, datetime.datetime):
            setattr(self, '_built', value)
        else:
            raise TypeError(
                f"Expected datetime.datetime or None but got '{value.__class__.__name__}' instead")

    @property
    def stability(self) -> str | None:
        return getattr(self, '_stability'), None

    @stability.setter
    def stability(self, value: str | None):
        if value is None:
            setattr(self, '_stability', None)
        elif value in [STABLE, EXPERIMENTAL, UNSTABLE, TESTING, SNAPSHOT]:
            setattr(self, '_stability', str(value))
        else:
            raise ValueError(
                f"Expected stable, experimenal, unstable, testing, snapshot or None but got '{value}' instead")

    @classmethod
    def from_json(cls, data: dict):
        self = cls.__new__(cls)
        if 'version' in data:
            self.version = data['version']
        if 'file' in data:
            self.file = data['file']
        if 'size' in data:
            self.size = Size.from_json(data['size'])
        if 'md5' in data:
            self.md5 = data['md5']
        if 'built' in data:
            self.built = datetime.datetime.fromtimestamp(data['built'] / 1e3)
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


def downloadJar(category: str, fp: str = None, version: str = None, finishcommand=None, block: bool = True) -> None | Jar:
    """
    Fetch a direct download link to a specific jar type with either the latest version or a specified one.

    Arguments
    ---
    `category` - The category of jars (spigot, bukkit, paper, etc..)

    `fp` - The destination file path.

    `version` - The version of the jar (don't provide for latest)

    `block` - When true it will wait until the file has finished downloading.

    `finishcommand` - Function to call when the jar has finished downloading.
    """

    def download(category, fp, version, callback):
        type = _type(category)
        details = fetchDetails(category, version)
        if fp is None:
            fp = os.path.join(os.getcwd(), details.file)
        res = requests.get(
            f'https://serverjars.com/api/fetchJar/{type}/{category}/{version}')
        with open(fp, 'wb') as jar:
            jar.write(res.content)
        if callback:
            callback(details)
        return details

    if version is None:
        version = ''

    if block:
        return download(category, fp, version, finishcommand)
    else:
        t = threading.Thread(target=download, args=(
            category, fp, version, finishcommand))
        t.start()


def fetchLatest(category: str) -> Jar:
    """
    Fetch details on the latest jar for a type

    Arguments
    ---
    `category` - The category of jars (spigot, bukkit, paper, etc..)

    """
    type = _type(category)
    res = sendRequest(f'fetchLatest/{type}/{category}')
    return Jar.from_json(res)


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
        jars.append(Jar.from_json(i))
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
    return Jar.from_json(res)
