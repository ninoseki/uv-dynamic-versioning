from functools import cached_property

from hatchling.version.source.plugin.interface import VersionSourceInterface
from returns.functions import raise_exception
from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import ResultE

from . import schemas
from .main import get_version, parse, read, validate


class DynamicVersionSource(VersionSourceInterface):
    PLUGIN_NAME = "uv-dynamic-versioning"

    @cached_property
    def project(self) -> schemas.Project:
        result: ResultE[schemas.Project] = flow(
            read(self.root), bind(parse), bind(validate)
        )
        return result.alt(raise_exception).unwrap()

    @property
    def config(self) -> schemas.UvDynamicVersioning:
        return self.project.tool.uv_dynamic_versioning or schemas.UvDynamicVersioning()

    def get_version_data(self) -> dict:
        result: ResultE[str] = get_version(self.config)
        version = result.alt(raise_exception).unwrap()
        return {"version": version}
