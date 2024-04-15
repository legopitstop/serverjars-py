from typing import Self
import requests
import os
import threading
import datetime
import subprocess
import logging
import sys

from .constants import *

ENDPOINT = "https://api.serverjars.com/api/"
TYPES = ["bedrock", "modded", "proxies", "servers", "vanilla"]

__version__ = "1.3.0"
__all__ = [
    "InvalidRequest",
    "JarNotFoundError",
    "Size",
    "Jar",
    "App",
    "download_jar",
    "fetch_latest",
    "fetch_all",
    "fetch_types",
    "fetch_details",
]


class InvalidRequest(Exception):
    pass


class JarNotFoundError(Exception):
    pass


class Size:
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
        return {"display": self.display, "bytes": self.bytes}

    @property
    def display(self) -> str:
        return getattr(self, "_display", "0.0 MB")

    @display.setter
    def display(self, value: str | None):
        if value is None:
            setattr(self, "_display", None)
        else:
            setattr(self, "_display", str(value))

    @property
    def bytes(self) -> int:
        return getattr(self, "_bytes", 0)

    @bytes.setter
    def bytes(self, value: int | None):
        if value is None:
            setattr(self, "_bytes", None)
        elif isinstance(value, int):
            setattr(self, "_bytes", value)
        else:
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )

    @classmethod
    def from_json(cls, data: dict):
        self = cls.__new__(cls)
        if "display" in data:
            self.display = data["display"]
        if "bytes" in data:
            self.bytes = data["bytes"]
        return self


class Jar:
    def __init__(
        self,
        version: str = None,
        file: str = None,
        size: Size = None,
        md5: str = None,
        built: int = None,
        stability: str = None,
    ):
        self.version: str = version
        self.file: str = file
        self.size: Size = size
        self.md5: str = md5
        self.built: int = built
        self.stability: str = stability

    def __str__(self):
        inner = ", ".join([f"{k}={v!r}" for k, v in self.__dict__.items()])
        return f"Jar({inner})"

    def __eq__(self, other):
        if isinstance(self, Jar):
            return (
                self.version == other.version
                and self.file == other.file
                and self.size == other.size
                and self.md5 == other.md5
                and self.built == other.built
                and self.stability == other.stability
            )
        return False

    @property
    def __dict__(self):
        return {
            "version": self.version,
            "file": self.file,
            "size": self.size.__dict__,
            "md5": self.md5,
            "built": self.built,
            "stability": self.stability,
        }

    @property
    def version(self) -> str | None:
        return getattr(self, "_version", None)

    @version.setter
    def version(self, value: str | None):
        if value is None:
            setattr(self, "_version", None)
        else:
            setattr(self, "_version", str(value))

    @property
    def file(self) -> str | None:
        return getattr(self, "_file", None)

    @file.setter
    def file(self, value: str | None):
        if value is None:
            setattr(self, "_file", None)
        else:
            setattr(self, "_file", str(value))

    @property
    def size(self) -> Size:
        return getattr(self, "_size", Size())

    @size.setter
    def size(self, value: Size | None):
        if value is None:
            setattr(self, "_size", Size())
        elif isinstance(value, Size):
            setattr(self, "_size", value)
        else:
            raise TypeError(
                f"Expected Size or None but got '{value.__class__.__name__}' instead"
            )

    @property
    def md5(self) -> str | None:
        return getattr(self, "_md5", None)

    @md5.setter
    def md5(self, value: str | None):
        if value is None:
            setattr(self, "_md5", None)
        else:
            setattr(self, "_md5", str(value))

    @property
    def built(self) -> datetime.datetime | None:
        return getattr(self, "_built", None)

    @built.setter
    def built(self, value: datetime.datetime | None):
        if value is None:
            setattr(self, "_built", None)
        elif isinstance(value, datetime.datetime):
            setattr(self, "_built", value)
        else:
            raise TypeError(
                f"Expected datetime.datetime or None but got '{value.__class__.__name__}' instead"
            )

    @property
    def stability(self) -> str | None:
        return getattr(self, "_stability"), None

    @stability.setter
    def stability(self, value: str | None):
        if value is None:
            setattr(self, "_stability", None)
        elif value in [STABLE, EXPERIMENTAL, UNSTABLE, TESTING, SNAPSHOT, RELEASE]:
            setattr(self, "_stability", str(value))
        else:
            raise ValueError(
                f"Expected stable, experimenal, unstable, testing, snapshot or None but got '{value}' instead"
            )

    @classmethod
    def from_json(cls, data: dict):
        self = cls.__new__(cls)
        if "version" in data:
            self.version = data["version"]
        if "file" in data:
            self.file = data["file"]
        if "size" in data:
            self.size = Size.from_json(data["size"])
        if "md5" in data:
            self.md5 = data["md5"]
        if "built" in data:
            self.built = datetime.datetime.fromtimestamp(data["built"] / 1e3)
        if "stability" in data:
            self.stability = data["stability"]
        return self


class App:
    def __init__(
        self,
        type: str,
        category: str,
        version: str = None,
        fp: str = "server.jar",
        logger: bool = True,
    ):
        self.type = type
        self.category = category
        self.fp = fp
        self.version = version
        if logger:
            logging.basicConfig(
                format="[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s",
                datefmt="%I:%M:%S",
                handlers=[logging.StreamHandler(sys.stdout)],
                level=logging.INFO,
            )

    @property
    def type(self) -> str:
        return getattr(self, "_type", None)

    @type.setter
    def type(self, value: str):
        setattr(self, "_type", str(value))

    @property
    def category(self) -> str | None:
        return getattr(self, "_category", None)

    @category.setter
    def category(self, value: str | None):
        if value is None:
            setattr(self, "_category", None)
        else:
            setattr(self, "_category", str(value))

    @property
    def fp(self) -> str | None:
        return getattr(self, "_fp", None)

    @fp.setter
    def fp(self, value: str | None):
        if value is None:
            setattr(self, "_value", None)
        else:
            setattr(self, "_fp", os.path.abspath(value))

    @property
    def version(self) -> str | None:
        return getattr(self, "_version", None)

    @version.setter
    def version(self, value: str | None):
        if value is None:
            setattr(self, "_version", None)
        else:
            setattr(self, "_version", str(value))

    @property
    def container(self) -> str | None:
        return getattr(self, "_container", os.path.dirname(self.fp))

    @container.setter
    def container(self, value: str | None):
        if value is None:
            setattr(self, "_container", os.path.dirname(self.fp))
        else:
            setattr(self, "_container", os.path.abspath(value))

    # Read-only

    @property
    def process(self) -> subprocess.Popen:
        return getattr(self, "_process", None)

    @classmethod
    def create(
        cls,
        type: str,
        category: str,
        version: str = None,
        fp: str = "server.jar",
        logger: bool = True,
    ) -> Self:
        """
        Create a new server

        :param category: The category of server to create
        :type category: str
        :param fp: The name of the jar, defaults to 'server.jar'
        :type fp: str, optional
        :param version: The Minecraft version of the jar, defaults to None
        :type version: str, optional
        :return: The created app
        :rtype: App
        """
        self = App(type, category, version, fp, logger)
        if not os.path.exists(self.fp):
            download_jar(self.type, self.category, self.fp, self.version)
        return self

    def get_docker(self) -> str:
        docker = os.path.expandvars(
            os.path.join(
                "%localappdata%",
                "Packages",
                "Microsoft.4297127D64EC6_8wekyb3d8bbwe",
                "LocalCache",
                "Local",
                "runtime",
                "java-runtime-gamma",
                "windows-x64",
                "java-runtime-gamma",
                "bin",
                "java.exe",
            )
        )
        if os.path.isfile(docker):
            return docker
        return "java"

    def run(self, args: list[str] = ["--nogui"]) -> int:
        """
        Run this server

        :type args: Args to start the server using. https://minecraft.wiki/w/Tutorials/Setting_up_a_server

        :return: The server that has started
        :rtype: App
        """
        docker = self.get_docker()
        cmd = ["cd", self.container, "&", docker, "-Xmx2G", "-jar", self.fp, *args]
        setattr(self, "_process", subprocess.Popen(cmd, shell=True))
        return self.process.wait()


def _send_request(*paths: str, **params):
    path = "/".join([str(p) for p in paths if p is not None])
    res = requests.get(ENDPOINT + path, params)
    if res.status_code == 200:
        data = res.json()
        return data.get("response")
    elif res.status_code == 404:
        raise JarNotFoundError(f"Jar not found! {path}")
    raise InvalidRequest(f"{res.status_code} Try again!")


def _download(type: str, category: str, version: str, fp: str, chunk_size: int):
    version = "" if version is None else "/" + version
    res = requests.get(
        ENDPOINT + f"fetchJar/{type}/{category}" + version,
        stream=True,
    )
    if res.status_code == 200:
        dir = os.path.dirname(fp)
        if dir:
            os.makedirs(dir, exist_ok=True)
        with open(fp, "wb") as fd:
            for chunk in res.iter_content(chunk_size=chunk_size):
                if chunk:
                    fd.write(chunk)
    else:
        data = res.json()
        raise InvalidRequest(data["error"]["message"])


def download_jar(
    type: str,
    category: str,
    fp: str = "server.jar",
    version: str = None,
    chunk_size: int = None,
    block: bool = True,
) -> None | Jar:
    """
    Fetch a direct download link to a specific jar type with either the latest version or a specified one

    :param category: The category of jars (spigot, bukkit, paper, etc..)
    :type category: str
    :param fp: The destination file path., defaults to None
    :type fp: str, optional
    :param version: The version of the jar (don't provide for latest), defaults to None
    :type version: str, optional
    :param block: When true it will wait until the file has finished downloading, defaults to True
    :type block: bool, optional
    :param chunk_size: Download the jar in chunks
    :type chunk_size: int, defaults to 1
    :return: The downloaded jar
    :rtype: None | Jar
    """
    if block:
        return _download(type, category, version, fp, chunk_size)
    else:
        t = threading.Thread(
            target=_download, args=(type, category, version, fp, chunk_size)
        )
        t.start()


def fetch_latest(type: str, category: str) -> Jar:
    """
    Fetch details on the latest jar for a type

    :param category: The category of jars (spigot, bukkit, paper, etc..)
    :type category: str
    :return: The latest jar
    :rtype: Jar
    """
    return Jar.from_json(_send_request("fetchLatest", type.lower(), category.lower()))


def fetch_all(type: str, category: str, max: int = 5) -> list[Jar]:
    """
    Fetch details on the all the jars for a type

    :param category: The category of jars (spigot, bukkit, paper, etc..)
    :type category: str
    :param max: The maximum amount of results to respond with. (Default: 5), defaults to 5
    :type max: int, optional
    :return: List of all jars
    :rtype: list[Jar]
    """
    res = _send_request("fetchAll", type.lower(), category.lower(), max=max)
    return [Jar.from_json(i) for i in res]


def fetch_types(type: str = "servers") -> list[str]:
    """
    Fetch a list of the possible jar categories

    :param type: The type of jars (bedrock, proxies, servers, etc...). Leave empty to see the list of all types, defaults to None
    :type type: str, optional
    :return: All categories for this type
    :rtype: list[str]
    """

    res = _send_request("fetchTypes", type.lower())
    return res.get("servers", [])


def fetch_details(type: str, category: str, version: str = None) -> Jar:
    """
    Fetch the details of a single jar

    :param category: The type of jars (servers, proxies, modded, etc..)
    :type category: str
    :param version: The version of the jar (don't provide for latest), defaults to None
    :type version: str, optional
    :return: Details about the jar
    :rtype: Jar
    """
    return Jar.from_json(
        _send_request("fetchDetails", type.lower(), category.lower(), version)
    )
