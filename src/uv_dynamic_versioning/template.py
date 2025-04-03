from __future__ import annotations

import contextlib
import os
import re
from datetime import datetime

import jinja2
from dunamai import (
    Version,
    bump_version,
    serialize_pep440,
    serialize_pvp,
    serialize_semver,
)


def base_part(base: str, index: int) -> int:
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


def render_template(
    template: str,
    *,
    version: Version,
) -> str:
    default_context = {
        "version": version,
        "base": version.base,
        "stage": version.stage,
        "revision": version.revision,
        "distance": version.distance,
        "commit": version.commit,
        "dirty": version.dirty,
        "branch": version.branch,
        "tagged_metadata": version.tagged_metadata,
        "branch_escaped": _escape_branch(version.branch),
        "timestamp": _format_timestamp(version.timestamp),
        "major": base_part(version.base, 0),
        "minor": base_part(version.base, 1),
        "patch": base_part(version.base, 2),
        "env": os.environ,
        "bump_version": bump_version,
        "serialize_pep440": serialize_pep440,
        "serialize_pvp": serialize_pvp,
        "serialize_semver": serialize_semver,
    }
    return jinja2.Template(template).render(**default_context)
