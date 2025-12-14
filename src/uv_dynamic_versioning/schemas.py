from __future__ import annotations

from dataclasses import dataclass, is_dataclass
from functools import cached_property
from typing import Any

from dunamai import Style, Vcs


def _normalize(cls, data: dict[str, Any]):
    """Filter dict keys to match dataclass fields and handle kebab-case to snake_case conversion with validation."""
    if not is_dataclass(cls):
        raise TypeError(f"{cls.__name__} is not a dataclass")

    fields = {f.name: f.type for f in cls.__dataclass_fields__.values()}
    result = {}
    for k, v in data.items():
        key = k.replace("-", "_")
        if key in fields:
            result[key] = v

    return result


@dataclass
class BumpConfig:
    enable: bool = False
    index: int = -1

    def _validate_enable(self):
        if not isinstance(self.enable, bool):
            raise ValueError("bump-config: enable must be a boolean")

    def _validate_index(self):
        if not isinstance(self.index, int):
            raise ValueError("bump-config: index must be an integer")

    def __post_init__(self):
        """Validate the bump configuration."""
        self._validate_enable()
        self._validate_index()

    @classmethod
    def from_dict(cls, data: dict) -> BumpConfig:
        """Create BumpConfig from dictionary with validation."""
        validated_data = _normalize(cls, data)
        return cls(**validated_data)


@dataclass
class FromFile:
    source: str
    pattern: str | None = None

    def _validate_source(self):
        if not isinstance(self.source, str):
            raise ValueError("source must be a string")

    def _validate_pattern(self):
        if self.pattern is not None and not isinstance(self.pattern, str):
            raise ValueError("pattern must be a string or None")

    def __post_init__(self):
        self._validate_source()
        self._validate_pattern()

    @classmethod
    def from_dict(cls, data: dict) -> FromFile:
        """Create FromFile from dictionary with validation."""
        validated_data = _normalize(cls, data)
        return cls(**validated_data)


@dataclass
class FormatJinjaImport:
    module: str
    item: str | None = None

    def _validate_module(self):
        if not isinstance(self.module, str):
            raise ValueError("module must be a string")

    def _validate_item(self):
        if self.item is not None and not isinstance(self.item, str):
            raise ValueError("item must be a string or None")

    def __post_init__(self):
        self._validate_module()
        self._validate_item()

    @classmethod
    def from_dict(cls, data: dict) -> FormatJinjaImport:
        validated_data = _normalize(cls, data)
        return cls(**validated_data)


@dataclass
class UvDynamicVersioning:
    vcs: Vcs = Vcs.Any
    metadata: bool | None = None
    tagged_metadata: bool = False
    dirty: bool = False
    pattern: str = "default"
    pattern_prefix: str | None = None
    format: str | None = None
    format_jinja: str | None = None
    format_jinja_imports: list[FormatJinjaImport] | None = None
    style: Style | None = None
    latest_tag: bool = False
    strict: bool = False
    tag_dir: str = "tags"
    tag_branch: str | None = None
    full_commit: bool = False
    ignore_untracked: bool = False
    commit_length: int | None = None
    commit_prefix: str | None = None
    escape_with: str | None = None
    bump: bool | BumpConfig = False
    fallback_version: str | None = None
    from_file: FromFile | None = None

    def _validate_vcs(self):
        if not isinstance(self.vcs, Vcs):
            raise ValueError(f"vcs is invalid - {self.vcs}")

    def _validate_metadata(self):
        if self.metadata is not None and not isinstance(self.metadata, bool):
            raise ValueError("metadata must be a boolean or None")

    def _validate_tagged_metadata(self):
        if not isinstance(self.tagged_metadata, bool):
            raise ValueError("tagged-metadata must be a boolean")

    def _validate_dirty(self):
        if not isinstance(self.dirty, bool):
            raise ValueError("dirty must be a boolean")

    def _validate_latest_tag(self):
        if not isinstance(self.latest_tag, bool):
            raise ValueError("latest-tag must be a boolean")

    def _validate_strict(self):
        if not isinstance(self.strict, bool):
            raise ValueError("strict must be a boolean")

    def _validate_full_commit(self):
        if not isinstance(self.full_commit, bool):
            raise ValueError("full-commit must be a boolean")

    def _validate_ignore_untracked(self):
        if not isinstance(self.ignore_untracked, bool):
            raise ValueError("ignore-untracked must be a boolean")

    def _validate_pattern(self):
        if self.pattern is not None and not isinstance(self.pattern, str):
            raise ValueError("pattern must be a string")

    def _validate_pattern_prefix(self):
        if self.pattern_prefix is not None and not isinstance(self.pattern_prefix, str):
            raise ValueError("pattern-prefix must be a string or None")

    def _validate_format(self):
        if self.format is not None and not isinstance(self.format, str):
            raise ValueError("format must be a string or None")

    def _validate_format_jinja(self):
        if self.format_jinja is not None and not isinstance(self.format_jinja, str):
            raise ValueError("format-jinja must be a string or None")

    def _validate_format_jinja_imports(self):
        if self.format_jinja_imports is not None:
            if not isinstance(self.format_jinja_imports, list):
                raise ValueError("format-jinja-imports must be a list or None")

            for item in self.format_jinja_imports:
                if not isinstance(item, FormatJinjaImport):
                    raise ValueError(
                        "format-jinja-imports must contain only FormatJinjaImport instances"
                    )

    def _validate_style(self):
        if self.style is not None and not isinstance(self.style, Style):
            raise ValueError(f"style is invalid - {self.style}")

    def _validate_tag_dir(self):
        if self.tag_dir is not None and not isinstance(self.tag_dir, str):
            raise ValueError("tag-dir must be a string")

    def _validate_tag_branch(self):
        if self.tag_branch is not None and not isinstance(self.tag_branch, str):
            raise ValueError("tag-branch must be a string or None")

    def _validate_commit_length(self):
        if self.commit_length is not None and not isinstance(self.commit_length, int):
            raise ValueError("commit-length must be an integer or None")

    def _validate_commit_prefix(self):
        if self.commit_prefix is not None and not isinstance(self.commit_prefix, str):
            raise ValueError("commit-prefix must be a string or None")

    def _validate_escape_with(self):
        if self.escape_with is not None and not isinstance(self.escape_with, str):
            raise ValueError("escape-with must be a string or None")

    def _validate_bump(self):
        if isinstance(self.bump, bool) and self.bump:
            self.bump = BumpConfig(enable=True)

        if isinstance(self.bump, dict):
            self.bump = BumpConfig.from_dict(self.bump)

        if not isinstance(self.bump, (bool, BumpConfig)):
            raise ValueError("bump must be a boolean or BumpConfig instance")

    def _validate_fallback_version(self):
        if self.fallback_version is not None and not isinstance(
            self.fallback_version, str
        ):
            raise ValueError("fallback-version must be a string or None")

    def __post_init__(self):
        """Validate the UvDynamicVersioning configuration."""
        self._validate_vcs()
        self._validate_metadata()
        self._validate_tagged_metadata()
        self._validate_dirty()
        self._validate_latest_tag()
        self._validate_strict()
        self._validate_full_commit()
        self._validate_ignore_untracked()
        self._validate_pattern()
        self._validate_pattern_prefix()
        self._validate_format()
        self._validate_format_jinja()
        self._validate_format_jinja_imports()
        self._validate_style()
        self._validate_tag_dir()
        self._validate_tag_branch()
        self._validate_commit_length()
        self._validate_bump()
        self._validate_fallback_version()
        self._validate_commit_prefix()
        self._validate_escape_with()

    @cached_property
    def bump_config(self) -> BumpConfig:
        if self.bump is False:
            return BumpConfig()

        if self.bump is True:
            return BumpConfig(enable=True)

        return self.bump

    @classmethod
    def from_dict(cls, data: dict) -> UvDynamicVersioning:
        """Create UvDynamicVersioning from dictionary with validation."""
        validated_data = _normalize(cls, data)

        # Special handling for enum fields
        if "vcs" in validated_data and isinstance(validated_data["vcs"], str):
            validated_data["vcs"] = Vcs(validated_data["vcs"])

        if "style" in validated_data and isinstance(validated_data["style"], str):
            validated_data["style"] = Style(validated_data["style"])

        # Special handling for bump field
        if "bump" in validated_data and isinstance(validated_data["bump"], dict):
            validated_data["bump"] = BumpConfig.from_dict(validated_data["bump"])

        if "from_file" in validated_data and isinstance(
            validated_data["from_file"], dict
        ):
            validated_data["from_file"] = FromFile.from_dict(
                validated_data["from_file"]
            )

        if "format_jinja_imports" in validated_data and isinstance(
            validated_data["format_jinja_imports"], list
        ):
            validated_data["format_jinja_imports"] = [
                FormatJinjaImport.from_dict(item)
                for item in validated_data["format_jinja_imports"]
                if isinstance(item, dict)
            ]

        return cls(**validated_data)


@dataclass
class Tool:
    uv_dynamic_versioning: UvDynamicVersioning | None = None

    def __post_init__(self):
        """Validate the Tool configuration."""
        if self.uv_dynamic_versioning is not None and not isinstance(
            self.uv_dynamic_versioning, UvDynamicVersioning
        ):
            raise ValueError(
                "uv-dynamic-versioning must be an instance of UvDynamicVersioning"
            )

    @classmethod
    def from_dict(cls, data: dict) -> Tool:
        """Create Tool from dictionary with validation."""
        validated_data = _normalize(cls, data)

        if "uv_dynamic_versioning" in validated_data and isinstance(
            validated_data["uv_dynamic_versioning"], dict
        ):
            validated_data["uv_dynamic_versioning"] = UvDynamicVersioning.from_dict(
                validated_data["uv_dynamic_versioning"]
            )

        return cls(**validated_data)


@dataclass
class Project:
    tool: Tool

    def _validate_tool(self):
        if not isinstance(self.tool, Tool):
            raise ValueError("tool must be an instance of Tool")

    def __post_init__(self):
        """Validate the Project configuration."""
        self._validate_tool()

    @classmethod
    def from_dict(cls, data: dict) -> Project:
        """Create Project from dictionary with validation."""
        validated_data = _normalize(cls, data)

        if "tool" in validated_data and isinstance(validated_data["tool"], dict):
            validated_data["tool"] = Tool.from_dict(validated_data["tool"])
        elif "tool" not in validated_data:
            raise ValueError("project must have a 'tool' field")

        return cls(**validated_data)


@dataclass
class MetadataHookConfig:
    dependencies: list[str] | None = None
    optional_dependencies: dict[str, list[str]] | None = None

    def _validate_dependencies(self):
        if self.dependencies is not None and not isinstance(self.dependencies, list):
            raise ValueError("dependencies must be a list or None")

        for v in self.dependencies or []:
            if not isinstance(v, str):
                raise ValueError("dependencies must be strings")

    def _validate_optional_dependencies(self):
        if self.optional_dependencies is None:
            return

        if not isinstance(self.optional_dependencies, dict):
            raise ValueError("optional-dependencies must be a dict or None")

        for key, value in self.optional_dependencies.items():
            if not isinstance(key, str):
                raise ValueError("optional-dependency keys must be strings")
            if not isinstance(value, list):
                raise ValueError("optional-dependency values must be lists of strings")

            for v in value:
                if not isinstance(v, str):
                    raise ValueError("optional-dependencies must be strings")

    def __post_init__(self):
        """Validate the MetadataHookConfig configuration."""
        self._validate_dependencies()
        self._validate_optional_dependencies()

    @classmethod
    def from_dict(cls, data: dict) -> MetadataHookConfig:
        """Create MetadataHookConfig from dictionary with validation."""
        validated_data = _normalize(cls, data)
        return cls(**validated_data)
