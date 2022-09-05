from .constants import Category, Type, Stability
import requests
import os

__all__ = [
    'downloadJar', 'fetchLatest','fetchAll','fetchTypes','fetchDetails'
]

class InvalidRequest(Exception): pass

class Size():
    def __init__(self, display=None, bytes=None):
        self.display = display
        self.bytes = bytes

    def json(self):
        return {
            'display': self.display,
            'bytes': self.bytes
        }

    def from_json(self, data:dict):
        if 'display' in data: self.display = data['display']
        if 'bytes' in data: self.bytes = data['bytes']
        return self
    
    def __str__(self):
        return self.display

class Jar():
    def __init__(self, version:str=None, file:str=None, size:Size=None, md5:str=None, built:int=None, stability:Stability=None):
        self.version = version
        self.file = file
        self.size = size
        self.md5 = md5
        self.built = built
        self.stability = stability

    def json(self):
        return {
            'version': self.version,
            'file': self.file,
            'size': self.size.json(),
            'md5': self.md5,
            'built': self.built,
            'stability': self.stability
        }

    def from_json(self, data:dict):
        if 'version' in data: self.version = data['version']
        if 'file' in data: self.file = data['file']
        if 'size' in data: self.size = Size().from_json(data['size'])
        if 'md5' in data: self.md5 = data['md5']
        if 'built' in data: self.built = data['built']
        if 'stability' in data: self.stability = Stability(data['stability'])
        return self

def _type(category:Category):
    DATA = {
        'nukkitx': Type.bedrock,
        'pocketmine': Type.bedrock,
        'MOHIST': Type.modded,
        'mohist': Type.modded,
        'catserver': Type.modded,
        'fabric': Type.modded,
        'bungeecord': Type.proxies,
        'velocity': Type.proxies,
        'waterfall': Type.proxies,
        'flamecord': Type.proxies,
        'bukkit': Type.servers,
        'paper': Type.servers,
        'spigot': Type.servers,
        'purpur': Type.servers,
        'tuinity': Type.servers,
        'sponge': Type.servers,
        'snapshot': Type.vanilla,
        'vanilla': Type.vanilla
    }
    res = DATA[str(category)]
    return res

def sendRequest(endpoint:str):
    res = requests.get('https://serverjars.com/api/'+endpoint)
    if res.status_code==200:
        data = res.json()
        return data['response']
    else:
        raise InvalidRequest(f'{res.status_code} Try again!')

def downloadJar(category:Category, file:str=None, version:str=''):
    """Fetch a direct download link to a specific jar type with either the latest version or a specified one."""
    type = _type(category)
    details = fetchDetails(category, version)
    if file is None: file = os.path.join(os.getcwd(), details.file)
    res = requests.get(f'https://serverjars.com/api/fetchJar/{type}/{category}/{version}')
    with open(file, 'wb') as jar: jar.write(res.content)
    return details

def fetchLatest(category:Category):
    """Fetch details on the latest jar for a type"""
    type = _type(category)
    res = sendRequest(f'fetchLatest/{type}/{category}')
    return Jar().from_json(res)

def fetchAll(category:Category, max:int=''):
    """Fetch details on the all the jars for a type"""
    type = _type(category)
    res = sendRequest(f'fetchAll/{type}/{category}/{max}')
    jars = []
    for i in res:
        jars.append(Jar().from_json(i))
    return jars

def fetchTypes(type:Type=''):
    """Fetch a list of the possible jar types."""
    res = sendRequest(f'fetchTypes/{type}')
    if type=='': return res
    else: return res[str(type)]

def fetchDetails(category:Category, version:str=''):
    """Fetch the details of a single jar."""
    type = _type(category)
    res = sendRequest(f'fetchDetails/{type}/{category}/{version}')
    return Jar().from_json(res)
