from functools import cached_property

from hatchling.version.source.plugin.interface import VersionSourceInterface
from returns.pipeline import flow

from . import schemas
from .main import get_version, parse, read, validate


class DynamicVersionSource(VersionSourceInterface):
    PLUGIN_NAME = "uv-dynamic-versioning"

    @cached_property
    def project(self) -> schemas.Project:
        return flow(read(self.root), parse, validate)

    @property
    def project_config(self) -> schemas.UvDynamicVersioning:
        return self.project.tool.uv_dynamic_versioning or schemas.UvDynamicVersioning()

    def get_version_data(self) -> dict:
        version = get_version(self.project_config)
        return {"version": version}
