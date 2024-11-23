from __future__ import annotations

from dunamai import Pattern, Style, Vcs
from pydantic import BaseModel, Field


class UvDynamicVersioning(BaseModel):
    vcs: Vcs = Vcs.Any
    metadata: bool | None = None
    tagged_metadata: bool = Field(default=False, alias="tagged-metadata")
    dirty: bool = False
    pattern: Pattern = Pattern.Default
    pattern_prefix: str | None = Field(default=None, alias="pattern-prefix")
    format: str | None = None
    style: Style | None = None
    latest_tag: bool = False
    strict: bool = False
    tag_dir: str = Field(default="tags", alias="tag-dir")
    tag_branch: str | None = Field(default=None, alias="tag-branch")
    full_commit: bool = Field(default=False, alias="full-commit")
    ignore_untracked: bool = Field(default=False, alias="ignore-untracked")
    bump: bool = False


class Tool(BaseModel):
    uv_dynamic_versioning: UvDynamicVersioning | None = Field(
        default=None, alias="uv-dynamic-versioning"
    )


class Project(BaseModel):
    tool: Tool
