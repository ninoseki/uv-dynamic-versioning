import os
from pathlib import Path

import tomlkit
from dunamai import Version
from returns.result import safe

from . import schemas


@safe
def read(root: str):
    pyproject = Path(root) / "pyproject.toml"
    return pyproject.read_text()


@safe
def parse(text: str):
    return tomlkit.parse(text)


@safe
def validate(project: tomlkit.TOMLDocument):
    return schemas.Project.model_validate(project.unwrap())


@safe
def get_version(config: schemas.UvDynamicVersioning) -> str:
    if "UV_DYNAMIC_VERSIONING_BYPASS" in os.environ:
        return os.environ["UV_DYNAMIC_VERSIONING_BYPASS"]

    version = Version.from_vcs(
        config.vcs,
        latest_tag=config.latest_tag,
        strict=config.strict,
        tag_branch=config.tag_branch,
        tag_dir=config.tag_dir,
        full_commit=config.full_commit,
        ignore_untracked=config.ignore_untracked,
        pattern=config.pattern,
        pattern_prefix=config.pattern_prefix,
    )

    return version.serialize(
        metadata=config.metadata,
        style=config.style,
        dirty=config.dirty,
        tagged_metadata=config.tagged_metadata,
        format=config.format,
        bump=config.bump,
    )
