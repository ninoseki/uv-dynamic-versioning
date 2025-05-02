from __future__ import annotations

import os
import re
from pathlib import Path

import tomlkit
from dunamai import _VALID_PEP440, _VALID_PVP, _VALID_SEMVER, Style, Version

from uv_dynamic_versioning.template import render_template

from . import schemas


def read(root: str):
    pyproject = Path(root) / "pyproject.toml"
    return pyproject.read_text()


def parse(text: str):
    return tomlkit.parse(text)


def validate(project: tomlkit.TOMLDocument):
    return schemas.Project.model_validate(project.unwrap())


def _get_bypassed_version() -> str | None:
    return os.environ.get("UV_DYNAMIC_VERSIONING_BYPASS")


def check_version_style(version: str, style: Style = Style.Pep440) -> None:
    """Check if a version is valid for a style."""
    name, pattern = {
        Style.Pep440: ("PEP 440", _VALID_PEP440),
        Style.SemVer: ("Semantic Versioning", _VALID_SEMVER),
        Style.Pvp: ("PVP", _VALID_PVP),
    }[style]
    failure_message = f"Version '{version}' does not conform to the {name} style"
    if not re.search(pattern, version):
        raise ValueError(failure_message)

    if style == Style.SemVer:
        parts = re.split(r"[.-]", version.split("+", 1)[0])
        if any(re.search(r"^0[0-9]+$", x) for x in parts):
            raise ValueError(failure_message)


def _get_version(config: schemas.UvDynamicVersioning) -> Version:
    try:
        return Version.from_vcs(
            config.vcs,
            latest_tag=config.latest_tag,
            strict=config.strict,
            tag_branch=config.tag_branch,
            tag_dir=config.tag_dir,
            full_commit=config.full_commit,
            ignore_untracked=config.ignore_untracked,
            pattern=config.pattern,
            pattern_prefix=config.pattern_prefix,
            commit_length=config.commit_length,
        )
    except RuntimeError as e:
        if fallback_version := config.fallback_version:
            return Version(fallback_version)
        raise e


def get_version(config: schemas.UvDynamicVersioning) -> tuple[str, Version]:
    bypassed = _get_bypassed_version()
    if bypassed:
        return bypassed, Version.parse(bypassed)

    version = _get_version(config)

    if config.format_jinja:
        updated = (
            version.bump(index=config.bump_config.index)
            if config.bump_config.enable and version.distance > 0
            else version
        )
        serialized = render_template(config.format_jinja, version=updated)
        if config.style:
            check_version_style(serialized, config.style)
    else:
        updated = (
            version.bump(smart=True, index=config.bump_config.index)
            if config.bump_config.enable
            else version
        )
        serialized = updated.serialize(
            metadata=config.metadata,
            style=config.style,
            dirty=config.dirty,
            tagged_metadata=config.tagged_metadata,
            format=config.format,
        )

    return (serialized, updated)
