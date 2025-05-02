from functools import cached_property
from typing import cast

from . import schemas
from .main import parse, read, validate


class BasePlugin:
    @cached_property
    def project(self) -> schemas.Project:
        text = read(cast(str, self.root))  # type: ignore
        parsed = parse(text)
        return validate(parsed)

    @property
    def project_config(self) -> schemas.UvDynamicVersioning:
        return self.project.tool.uv_dynamic_versioning or schemas.UvDynamicVersioning()
