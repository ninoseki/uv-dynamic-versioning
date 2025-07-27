from __future__ import annotations

from functools import cached_property
from dataclasses import dataclass, field

from dunamai import Style, Vcs


def _filter_dict(cls, data: dict):
    valid_fields = {f.name for f in cls.__dataclass_fields__.values()}

    result = {}
    for k, v in data.items():
        key = k.replace("-", "_")
        if key in valid_fields:
            result[key] = v
    return result


@dataclass
class BumpConfig:
    enable: bool = False
    index: int = -1

    @classmethod
    def model_validate(cls, data: dict):
        return cls(**_filter_dict(cls, data or {}))


@dataclass
class UvDynamicVersioning:
    vcs: Vcs = Vcs.Any
    metadata: bool | None = None
    tagged_metadata: bool = field(default=False)
    dirty: bool = False
    pattern: str = "default"
    pattern_prefix: str | None = field(default=None)
    format: str | None = None
    format_jinja: str | None = field(default=None)
    style: Style | None = None
    latest_tag: bool = False
    strict: bool = False
    tag_dir: str = field(default="tags")
    tag_branch: str | None = field(default=None)
    full_commit: bool = field(default=False)
    ignore_untracked: bool = field(default=False)
    commit_length: int | None = field(default=None)
    bump: bool | BumpConfig = False
    fallback_version: str | None = field(default=None)

    @cached_property
    def bump_config(self) -> BumpConfig:
        if self.bump is False:
            return BumpConfig()

        if self.bump is True:
            return BumpConfig(enable=self.bump)

        return self.bump

    @classmethod
    def model_validate(cls, data: dict):
        data = _filter_dict(cls, data or {})
        if "vcs" in data and isinstance(data["vcs"], str):
            data["vcs"] = Vcs(data["vcs"])
        if "style" in data and isinstance(data["style"], str):
            try:
                data["style"] = Style(data["style"])
            except ValueError:
                data["style"] = None
        return cls(**data)


@dataclass
class Tool:
    uv_dynamic_versioning: UvDynamicVersioning | None = field(default=None)

    @classmethod
    def model_validate(cls, data: dict):
        data = _filter_dict(cls, data or {})
        if "uv_dynamic_versioning" in data and isinstance(
            data["uv_dynamic_versioning"], dict
        ):
            data["uv_dynamic_versioning"] = UvDynamicVersioning.model_validate(
                data["uv_dynamic_versioning"]
            )
        return cls(**data)


@dataclass
class Project:
    tool: Tool

    @classmethod
    def model_validate(cls, data: dict):
        data = _filter_dict(cls, data or {})
        if "tool" in data and isinstance(data["tool"], dict):
            data["tool"] = Tool.model_validate(data["tool"])
        return cls(**data)

@dataclass
class MetadataHookConfig:
    dependencies: list[str] | None = None
    optional_dependencies: dict[str, list[str]] | None = field(default=None)

    @classmethod
    def model_validate(cls, data: dict):
        return cls(**_filter_dict(cls, data or {}))
