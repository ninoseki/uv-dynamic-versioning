from hatchling.version.source.plugin.interface import VersionSourceInterface

from .base import BasePlugin


class DynamicVersionSource(BasePlugin, VersionSourceInterface):
    PLUGIN_NAME = "uv-dynamic-versioning"

    def get_version_data(self) -> dict:
        version = self.get_version()
        return {"version": version}
