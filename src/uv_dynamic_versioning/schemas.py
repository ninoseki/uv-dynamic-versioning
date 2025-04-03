from __future__ import annotations

from functools import cached_property

from dunamai import Pattern, Style, Vcs
from pydantic import BaseModel, Field


class BumpConfig(BaseModel):
    enable: bool = False
    index: int = -1


class UvDynamicVersioning(BaseModel):
    vcs: Vcs = Vcs.Any
    metadata: bool | None = None
    tagged_metadata: bool = Field(default=False, alias="tagged-metadata")
    dirty: bool = False
    pattern: Pattern = Pattern.Default
    pattern_prefix: str | None = Field(default=None, alias="pattern-prefix")
    format: str | None = None
    format_jinja: str | None = Field(default=None, alias="format-jinja")
    style: Style | None = None
    latest_tag: bool = False
    strict: bool = False
    tag_dir: str = Field(default="tags", alias="tag-dir")
    tag_branch: str | None = Field(default=None, alias="tag-branch")
    full_commit: bool = Field(default=False, alias="full-commit")
    ignore_untracked: bool = Field(default=False, alias="ignore-untracked")
    bump: bool | BumpConfig = False

    @cached_property
    def bump_config(self) -> BumpConfig:
        if self.bump is False:
            return BumpConfig()

        if self.bump is True:
            return BumpConfig(enable=self.bump)

        return self.bump


class Tool(BaseModel):
    uv_dynamic_versioning: UvDynamicVersioning | None = Field(
        default=None, alias="uv-dynamic-versioning"
    )


class Project(BaseModel):
    tool: Tool


class MetadataHookConfig(BaseModel):
    dependencies: list[str] | None = None
    optional_dependencies: dict[str, list[str]] | None = Field(
        default=None, alias="optional-dependencies"
    )
