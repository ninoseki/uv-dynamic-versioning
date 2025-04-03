import os
from pathlib import Path

import tomlkit
from dunamai import Version

from uv_dynamic_versioning.template import render_template

from . import schemas


def read(root: str):
    pyproject = Path(root) / "pyproject.toml"
    return pyproject.read_text()


def parse(text: str):
    return tomlkit.parse(text)


def validate(project: tomlkit.TOMLDocument):
    return schemas.Project.model_validate(project.unwrap())


def _get_version(config: schemas.UvDynamicVersioning) -> Version:
    if "UV_DYNAMIC_VERSIONING_BYPASS" in os.environ:
        return Version.parse(os.environ["UV_DYNAMIC_VERSIONING_BYPASS"])

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
    version = _get_version(config)

    if config.format_jinja:
        # NOTE: don't know why but poetry-dynamic-versioning check bump_config and also distance when using Jinja2
        #       so follow it
        updated = (
            version.bump(smart=True, index=config.bump_config.index)
            if config.bump_config.enable and version.distance > 0
            else version
        )
        return (
            render_template(config.format_jinja, version=updated),
            updated,
        )

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
