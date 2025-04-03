from hatchling.version.source.plugin.interface import VersionSourceInterface

from .base import BasePlugin
from .main import get_version


class DynamicVersionSource(BasePlugin, VersionSourceInterface):
    PLUGIN_NAME = "uv-dynamic-versioning"

    def get_version_data(self) -> dict[str, str]:
        version = get_version(self.project_config)[0]
        return {"version": version}
