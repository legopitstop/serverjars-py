"""
Download and fetch details about Minecraft server jars.
"""

__version__ = "1.4.0"

__all__ = [
    "BEDROCK",
    "MODDED",
    "PROXIES",
    "VANILLA",
    "BANNER",
    "FABRIC",
    "MOHIST",
    "RELEASE",
    "SNAPSHOT",
    "register",
    "download_jar",
    "fetch_all_types",
    "fetch_all",
    "fetch_details",
    "fetch_jar",
    "fetch_latest",
    "fetch_types",
    "get_manifest",
    "SoftwareFileSize",
    "SoftwareFile",
    "SoftwareBuilder",
    "InvalidRequest",
    "JarNotFoundError",
    "MohistAPIService",
    "BannerService",
    "FabricService",
    "MohistService",
    "MinecraftServiceBase",
    "ReleaseService",
    "SnapshotService",
]

# load services

from .software import (
    register,
    download_jar,
    fetch_all_types,
    fetch_all,
    fetch_details,
    fetch_jar,
    fetch_latest,
    fetch_types,
    SoftwareFileSize,
    SoftwareFile,
    SoftwareBuilder,
)
from .exception import InvalidRequest, JarNotFoundError
from .constants import (
    BEDROCK,
    MODDED,
    PROXIES,
    VANILLA,
    BANNER,
    FABRIC,
    MOHIST,
    RELEASE,
    SNAPSHOT,
)
from .modded import MohistAPIService, BannerService, FabricService, MohistService
from .vanilla import get_manifest, MinecraftServiceBase, ReleaseService, SnapshotService

# from .bedrock import *
# from .proxies import *
# from .servers import *
