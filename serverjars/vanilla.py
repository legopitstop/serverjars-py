from typing import Any, List
from datetime import datetime
import requests

from . import register, InvalidRequest, SoftwareBuilder

__all__ = ["get_manifest", "MinecraftServiceBase", "ReleaseService", "SnapshotService"]


def get_manifest() -> dict[str, Any]:
    res = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    if res.status_code == 200:
        return res.json()
    raise InvalidRequest(res.text)


def _release_versions() -> dict[str, str]:
    data = {}
    versions = [x for x in get_manifest()["versions"] if x["type"] == "release"]
    for v in versions:
        data[v["id"]] = v["url"]
    return data


def _versions() -> dict[str, str]:
    data = {}
    for v in get_manifest()["versions"]:
        data[v["id"]] = v["url"]
    return data


class MinecraftServiceBase(SoftwareBuilder):
    """
    https://mojang.com
    """

    release_only = True
    type = "vanilla"

    def available_versions(self) -> List[str]:
        if self.release_only:
            return list(_release_versions().keys())
        return list(_versions().keys())

    def get_meta(self, version: str) -> dict[str, Any]:
        meta = {"hash": None, "origin": None, "stability": None, "created": None}
        if version == "latest":
            manifest_url = _versions()[get_manifest()["latest"]["release"]]
        else:
            manifest_url = _versions()[version]
        res = requests.get(manifest_url)
        if res.status_code == 200:
            data = res.json()
            server_manifest = data["downloads"]["server"]
            meta["hash"] = server_manifest["sha1"]
            meta["origin"] = server_manifest["url"]
            meta["stability"] = data["type"]
            meta["created_at"] = data["time"]
            return meta
        raise InvalidRequest(res.text)

    def get_hash(self, version: str) -> str:
        return self.get_meta(version)["hash"]

    def get_built(self, version: str) -> datetime:
        return self.get_meta(version)["created_at"]

    def get_download(self, version: str) -> str:
        return self.get_meta(version)["origin"]

    def get_stability(self, version: str) -> str:
        return self.get_meta(version)["stability"]


@register
class ReleaseService(MinecraftServiceBase):
    category = "release"


@register
class SnapshotService(MinecraftServiceBase):
    release_only = False
    category = "snapshot"
