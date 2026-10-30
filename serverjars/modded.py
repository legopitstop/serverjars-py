from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import hashlib
import requests

from .exception import InvalidRequest
from .software import MAX_FETCH_WORKERS, register, SoftwareBuilder

__all__ = ["MohistAPIService", "BannerService", "FabricService", "MohistService"]


class MohistAPIService:
    def __init__(self, project: str):
        self.project = project

    def _builds(self, version: str) -> List[Dict[str, Any]]:
        res = requests.get(
            f"https://mohistmc.com/api/v2/projects/{self.project}/{version}/builds"
        )
        if res.status_code == 200:
            return res.json()["builds"]
        raise InvalidRequest(res.text)

    def available_versions(self) -> List[str]:
        res = requests.get(f"https://mohistmc.com/api/v2/projects/{self.project}")
        if res.status_code != 200:
            raise InvalidRequest(res.text)
        versions = list(reversed(res.json()["versions"]))
        with ThreadPoolExecutor(max_workers=MAX_FETCH_WORKERS) as pool:
            has_builds = list(pool.map(lambda v: bool(self._builds(v)), versions))
        return [v for v, ok in zip(versions, has_builds) if ok]

    def get_meta(self, version) -> Dict[str, Any]:
        builds = self._builds(version)
        if not builds:
            raise InvalidRequest(f"No builds for {self.project} {version}")
        latest_build = builds[-1]
        return {
            "build": latest_build["gitSha"],
            "hash": latest_build["fileMd5"],
            "origin": latest_build["url"],
            "created_at": latest_build["createdAt"],
        }


@register
class BannerService(SoftwareBuilder):
    """
    https://mohistmc.com/
    """

    type = "modded"
    category = "banner"

    api = MohistAPIService(category)

    def available_versions(self) -> List[str]:
        return self.api.available_versions()

    def get_meta(self, version: str) -> Dict[str, Any]:
        return self.api.get_meta(version)

    def get_hash(self, version: str, meta: Dict[str, Any]) -> str:
        return meta["hash"]

    def get_built(self, version: str, meta: Dict[str, Any]) -> datetime:
        return meta["created_at"]

    def get_download(self, version: str, meta: Dict[str, Any]) -> str:
        return meta["origin"]

    def get_stability(self, version: str, meta: Dict[str, Any]) -> str:
        return "unknown"


@register
class FabricService(SoftwareBuilder):
    """
    https://fabricmc.net
    """

    type = "modded"
    category = "fabric"

    def available_versions(self) -> List[str]:
        res = requests.get("https://meta.fabricmc.net/v2/versions/game")
        if res.status_code == 200:
            data = res.json()
            return [x["version"] for x in data if x["stable"]]
        raise InvalidRequest(res.text)

    def get_latest_installer(self) -> Dict[str, Any]:
        res = requests.get("https://meta.fabricmc.net/v2/versions/installer")
        if res.status_code == 200:
            data = res.json()
            for k in data:
                if k["stable"]:
                    return k
        raise InvalidRequest(res.text)

    def get_latest_loader(self) -> Dict[str, Any]:
        res = requests.get("https://meta.fabricmc.net/v2/versions/loader")
        if res.status_code == 200:
            data = res.json()
            for k in data:
                if k["stable"]:
                    return k
        raise InvalidRequest(res.text)

    def get_meta(self, version: str) -> Dict[str, Any]:
        loader = self.get_latest_loader()
        return {
            "installer": self.get_latest_installer()["version"],
            "loader": loader["version"],
            "loader_build": loader["build"],
        }

    def get_hash(self, version: str, meta: Dict[str, Any]) -> str:
        if "loader" not in meta or "installer" not in meta:
            return ""
        else:
            loader = meta["loader"]
            installer = meta["installer"]
            res = requests.get(
                f"https://meta.fabricmc.net/v2/versions/loader/{ version }/{ loader }/{ installer }/server/jar"
            )
            if res.status_code == 200:
                return str(hashlib.sha256(res.content))
            raise InvalidRequest(res.text)

    def get_download(self, version: str, meta: Dict[str, Any]) -> str:
        loader = meta["loader"]
        installer = meta["installer"]
        return f"https://meta.fabricmc.net/v2/versions/loader/{ version }/{ loader }/{ installer }/server/jar"

    def get_stability(self, version: str, meta: Dict[str, Any]) -> str:
        return "stable"

    def get_built(self, version: str, meta: Dict[str, Any]) -> datetime:
        return datetime.now()


# TODO
# @register
# class ForgeService(SoftwareBuilder):
#     type = "modded"
#     category = "forge"


@register
class MohistService(SoftwareBuilder):
    """
    https://mohistmc.com/
    """

    type = "modded"
    category = "mohist"
    api = MohistAPIService(category)

    def available_versions(self) -> List[str]:
        return self.api.available_versions()

    def get_meta(self, version: str) -> Dict[str, Any]:
        return self.api.get_meta(version)

    def get_hash(self, version: str, meta: Dict[str, Any]) -> str:
        return meta["hash"]

    def get_built(self, version: str, meta: Dict[str, Any]) -> datetime:
        return meta["created_at"]

    def get_download(self, version: str, meta: Dict[str, Any]) -> str:
        return meta["origin"]

    def get_stability(self, version: str, meta: Dict[str, Any]) -> str:
        return "unknown"
