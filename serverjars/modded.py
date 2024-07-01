from typing import Any, Dict, List
from datetime import datetime
import hashlib
import requests

from . import register, InvalidRequest, SoftwareBuilder

__all__ = ["MohistAPIService", "BannerService", "FabricService", "MohistService"]


class MohistAPIService:
    def __init__(self, project: str):
        self.project = project

    def available_versions(self) -> List[str]:
        res = requests.get(f"https://mohistmc.com/api/v2/projects/{self.project}")
        if res.status_code == 200:
            data = res.json()
            data["versions"].reverse()
            return data["versions"]
        raise InvalidRequest(res.text)

    def get_meta(self, version) -> Dict[str, Any]:
        meta = {}
        res = requests.get(
            f"https://mohistmc.com/api/v2/projects/{self.project}/{version}/builds"
        )
        if res.status_code == 200:
            data = res.json()
            latest_build = data["builds"][-1]
            meta["build"] = latest_build["number"]
            meta["hash"] = latest_build["fileMd5"]
            meta["origin"] = latest_build["url"]
            meta["created_at"] = latest_build["createdAt"]
            return meta
        raise InvalidRequest(res.text)


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

    def get_meta(self, version: str) -> dict[str, Any]:
        return self.api.get_meta(version)

    def get_hash(self, version: str) -> str:
        return self.get_meta(version)["hash"]

    def get_built(self, version: str) -> datetime:
        return self.get_meta(version)["created_at"]

    def get_download(self, version: str) -> str:
        return self.get_meta(version)["origin"]

    def get_stability(self, version: str) -> str:
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

    def get_latest_installer(self) -> dict[str, Any]:
        res = requests.get("https://meta.fabricmc.net/v2/versions/installer")
        if res.status_code == 200:
            data = res.json()
            for k in data:
                if k["stable"]:
                    return k
        raise InvalidRequest(res.text)

    def get_latest_loader(self) -> dict[str, Any]:
        res = requests.get("https://meta.fabricmc.net/v2/versions/loader")
        if res.status_code == 200:
            data = res.json()
            for k in data:
                if k["stable"]:
                    return k
        raise InvalidRequest(res.text)

    def get_meta(self, version: str) -> dict[str, Any]:
        meta = {}
        meta["installer"] = self.get_latest_installer()["version"]
        meta["loader"] = self.get_latest_loader()["version"]
        meta["loader_build"] = self.get_latest_loader()["build"]
        return meta

    def get_hash(self, version: str) -> str:
        meta = self.get_meta(version)
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

    def get_download(self, version: str) -> str:
        meta = self.get_meta(version)
        loader = meta["loader"]
        installer = meta["installer"]
        return f"https://meta.fabricmc.net/v2/versions/loader/{ version }/{ loader }/{ installer }/server/jar"

    def get_stability(self, version: str) -> str:
        return "stable"

    def get_built(self, version: str) -> datetime:
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

    def get_meta(self, version: str) -> dict[str, Any]:
        return self.api.get_meta(version)

    def get_hash(self, version: str) -> str:
        return self.get_meta(version)["hash"]

    def get_built(self, version: str) -> datetime:
        return self.get_meta(version)["created_at"]

    def get_download(self, version: str) -> str:
        return self.get_meta(version)["origin"]

    def get_stability(self, version: str) -> str:
        return "unknown"
