from hatchling.version.source.plugin.interface import VersionSourceInterface

from .base import BasePlugin
from .main import get_version


class DynamicVersionSource(BasePlugin, VersionSourceInterface):
    PLUGIN_NAME = "uv-dynamic-versioning"

    def get_version_data(self) -> dict[str, str]:
        version, _ = get_version(self.project_config)
        return {"version": version}
