from functools import cached_property

from returns.pipeline import flow

from . import schemas
from .main import parse, read, validate


class BasePlugin:
    @cached_property
    def project(self) -> schemas.Project:
        root: str = self.root  # type: ignore
        return flow(read(root), parse, validate)

    @property
    def project_config(self) -> schemas.UvDynamicVersioning:
        return self.project.tool.uv_dynamic_versioning or schemas.UvDynamicVersioning()
