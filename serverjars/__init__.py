"""
Download and fetch details about Minecraft server jars.
"""

from typing import Any, Dict, List
from pydantic import BaseModel
from datetime import datetime
import threading
import requests
import os

__all__ = [
    "__version__",
    "register",
    "SoftwareFileSize",
    "SoftwareFile",
    "SoftwareBuilder",
    "download_jar",
    "fetch_all_types",
    "fetch_all",
    "fetch_details",
    "fetch_jar",
    "fetch_latest",
    "fetch_types",
]
__version__ = "1.4.0"


def register(cls):
    def wrapper():
        if not issubclass(cls, SoftwareBuilder):
            raise TypeError("Expected SoftwareBuilder")
        global SERVICES
        key = cls.type.lower()
        if key not in SERVICES:
            SERVICES[key] = []
        SERVICES[key].append(cls())
        return cls

    return wrapper()


class SoftwareFileSize(BaseModel):
    bytes: int
    display: str

    def __str__(self) -> str:
        return self.display


class SoftwareFile(BaseModel):
    version: str
    stability: str
    hash: str
    download: str
    meta: Dict[str, Any]
    built: datetime
    size: SoftwareFileSize


class SoftwareBuilder:
    type: str = ""
    category: str = ""

    def __str__(self) -> str:
        return (
            self.__class__.__name__
            + f"(type={ repr(self.type) }, category={ repr(self.category) })"
        )

    def available_versions(self) -> List[str]:
        raise NotImplementedError()

    def get_version(self, version: str) -> str:
        if version == "latest":
            return self.available_versions()[0]
        return version

    def get_meta(self, version: str) -> Dict[str, Any]:
        raise NotImplementedError()

    def get_hash(self, version: str) -> str:
        raise NotImplementedError()

    def get_download(self, version: str) -> str:
        raise NotImplementedError()

    def get_built(self, version: str) -> datetime:
        raise NotImplementedError()

    def get_stability(self, version: str) -> str:
        raise NotImplementedError()

    def build(self, version: str) -> SoftwareFile:
        version = self.get_version(version)
        hash = self.get_hash(version)
        if not hash:
            raise Exception(f"Failed to find hash for version {version}")
        download = self.get_download(version)
        if not download:
            raise Exception(f"Failed to find download for version {version}")
        bytes = int(requests.head(download).headers.get("Content-length", 0))
        meta = self.get_meta(version)
        if not meta:
            raise Exception(f"Failed to find meta for version {version}")
        return SoftwareFile(
            version=version,
            stability=self.get_stability(version),
            hash=hash,
            meta=meta,
            download=download,
            built=self.get_built(version),
            size=SoftwareFileSize(
                bytes=bytes,
                display="%.2f MiB" % (bytes / 1024.0 / 1024.0),
            ),
        )


SERVICES: Dict[str, List[SoftwareBuilder]] = {}

# load services

from .constants import *
from .exception import *
from .modded import *
from .vanilla import *

# from .bedrock import *
# from .proxies import *
# from .servers import *


def _download(type: str, category: str, version: str, fp: str, chunk_size: int) -> None:
    res = fetch_jar(type, category, version)
    dir = os.path.dirname(fp)
    if dir:
        os.makedirs(dir, exist_ok=True)
    with open(fp, "wb") as fd:
        for chunk in res.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)


def download_jar(
    type: str,
    category: str,
    version: str = "latest",
    fp: str = "server.jar",
    chunk_size: int = 1000000,
    block: bool = True,
) -> None:
    """
    Download a server jar file.

    :param type: The type of jar.
    :type type: str
    :param category: The category of jar.
    :type category: str
    :param version: The version of the jar, defaults of "latest"
    :type version: str
    :param fp: The file path of the jar, defaults to "server.jar"
    :type fp: str, optional
    :param chunk_size: The size of each chunk to download, defaults to 1000000 (1 MB)
    :type chunk_size: int, optional
    :param block: When true it will stop the rest of the script from running, defaults to True

    :type block: bool, optional
    """
    type = type.lower()
    if block:
        _download(type, category, version, fp, chunk_size)
    else:
        t = threading.Thread(
            target=_download, args=(type, category, version, fp, chunk_size)
        )
        t.start()


def fetch_all_types() -> Dict[str, List[str]]:
    """
    All types and categories.

    :rtype: dict[str, list[str]]
    """
    res = {}
    for k, v in SERVICES.items():
        res[k] = [x.category for x in v]
    return res


def fetch_all(type: str, category: str, max: int) -> List[SoftwareFile]:
    """
    Fetch a list of jar files.

    :param type: The type of jar
    :type type: str
    :param category: The category of jar
    :type category: str
    :param max: The max number of jars to fetch
    :type max: int

    :return: All fetched jars
    :rtype: list[SoftwareFile]
    """
    type = type.lower()
    res = SERVICES.get(type, None)
    if not res:
        raise JarNotFoundError(type)
    for c in res:
        if c.category == category:
            return [
                fetch_details(type, category, version)
                for version in c.available_versions()[:max]
            ]
    raise JarNotFoundError(type)


def fetch_details(type: str, category: str, version: str = "latest") -> SoftwareFile:
    """
    Get details about a jar file.

    :param type: The type of jar.
    :type type: str
    :param category: The category of jar.
    :type category: str
    :param version: The version of jar.
    :type version: str

    :return: Details about the jar.
    :rtype: SoftwareFile
    """
    type = type.lower()
    res = SERVICES.get(type, None)
    if not res:
        raise JarNotFoundError(type)
    for c in res:
        if c.category == category:
            return c.build(version)
    raise JarNotFoundError(type)


def fetch_jar(type: str, category: str, version: str = "latest") -> requests.Response:
    """
    Fetch the jar file.

    :param type: The type of jar.
    :type type: str
    :param category: The category of jar.
    :type category: str
    :param version: The version of jar, defaults to "latest"
    :type version: str, optional

    :return: The requested jar.
    :rtype: requests.Response
    """
    details = fetch_details(type.lower(), category, version)
    res = requests.get(details.download, stream=True)
    if res.status_code == 200:
        return res
    raise InvalidRequest(res.text)


def fetch_latest(type: str, category: str) -> SoftwareFile:
    """
    Fetch the jar.

    :param type: The type of jar.
    :type type: str
    :param category: The category of jar.
    :type category: str

    :return: The latest jar.
    :rtype: SoftwareFile
    """
    return fetch_details(type, category, "latest")


def fetch_types(type: str) -> List[str]:
    """
    Get categories for type.

    :param type: The type of jar.
    :type type: str

    :return: All categories for this type.
    :rtype: list
    """
    return fetch_all_types()[type.lower()]
