from __future__ import annotations

import contextlib
import os
import re
from datetime import datetime
from typing import Callable

import jinja2
from dunamai import (
    Version,
    bump_version,
    serialize_pep440,
    serialize_pvp,
    serialize_semver,
)
from pydantic import BaseModel, ConfigDict, Field

from . import schemas


def render_jinja(
    version: Version,
    config: schemas.UvDynamicVersioning,
) -> str:
    if config.bump and version.distance > 0:
        version = version.bump(smart=True)

    default_context = _JinjaDefaultContext.from_version(version).model_dump()

    return jinja2.Template(config.format_jinja).render(**default_context)


class _JinjaDefaultContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    version: Version
    base: str | None = Field(default=None)
    stage: str | None = Field(default=None)
    revision: int | None = Field(default=None)
    distance: int | None = Field(default=None)
    commit: str | None = Field(default=None)
    dirty: bool | None = Field(default=None)
    branch: str | None = Field(default=None)
    tagged_metadata: str | None = Field(default=None)
    branch_escaped: str | None = Field(default=None)
    timestamp: str | None = Field(default=None)
    major: int | None = Field(default=None)
    minor: int | None = Field(default=None)
    patch: int | None = Field(default=None)
    env: os._Environ[str] = Field(default=os.environ)
    bump_version: Callable[[Version, bool], Version] = Field(default=bump_version)
    serialize_pep440: Callable[[Version], str] = Field(default=serialize_pep440)
    serialize_pvp: Callable[[Version], str] = Field(default=serialize_pvp)
    serialize_semver: Callable[[Version], str] = Field(default=serialize_semver)

    @classmethod
    def from_version(cls, version: Version) -> _JinjaDefaultContext:
        return cls(
            version=version,
            base=version.base,
            stage=version.stage,
            revision=version.revision,
            distance=version.distance,
            commit=version.commit,
            dirty=version.dirty,
            branch=version.branch,
            tagged_metadata=version.tagged_metadata,
            branch_escaped=_escape_branch(version.branch),
            timestamp=_format_timestamp(version.timestamp),
            major=_base_part(version.base, 0),
            minor=_base_part(version.base, 1),
            patch=_base_part(version.base, 2),
        )


def _base_part(base: str, index: int) -> int:
    parts = base.split(".")
    result = 0

    with contextlib.suppress(KeyError, ValueError):
        result = int(parts[index])

    return result


def _escape_branch(value: str | None) -> str | None:
    if value is None:
        return None
    return re.sub(r"[^a-zA-Z0-9]", "", value)


def _format_timestamp(value: datetime | None) -> str | None:
    if value is None:
        return None

    return value.strftime("%Y%m%d%H%M%S")
