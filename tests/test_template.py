from datetime import datetime, timezone

import pytest
from dunamai import Version

from uv_dynamic_versioning import schemas, template


@pytest.fixture
def version():
    return Version(
        base="1.0.0",
        stage=("alpha", 1),
        distance=0,
        commit="message",
        dirty=False,
        branch="main",
        timestamp=datetime(2025, 4, 1, 12, 0, 0, tzinfo=timezone.utc),
    )


@pytest.fixture
def config():
    return schemas.UvDynamicVersioning.model_validate(
        {
            "format-jinja": "{{- base }}",
        }
    )


def test_when_rendering_basic_version_then_returns_base_version(
    version: Version,
    config: schemas.UvDynamicVersioning,
):
    result = template.render_jinja(version, config)

    assert result == "1.0.0"


def test_when_bumping_version_then_returns_bumped_version(
    version: Version,
    config: schemas.UvDynamicVersioning,
):
    version.distance = 2
    version.revision = 1
    config.bump = True
    config.format_jinja = "{{- base }}+r{{- revision }}"

    result = template.render_jinja(version, config)

    assert result == "1.0.0+r2"


def test_when_rendering_version_with_stage_and_revision_then_returns_formatted_version(
    version: Version,
    config: schemas.UvDynamicVersioning,
):
    config.format_jinja = "{{- base }}{{- stage }}{{- revision }}"

    result = template.render_jinja(version, config)

    assert result == "1.0.0alpha1"


def test_when_rendering_version_with_commit_and_branch_then_returns_formatted_version(
    version: Version,
    config: schemas.UvDynamicVersioning,
):
    config.format_jinja = "{{- commit }}-{{- branch }}"

    result = template.render_jinja(version, config)

    assert result == "message-main"


def test_when_rendering_version_with_timestamp_then_returns_formatted_timestamp(
    version: Version, config: schemas.UvDynamicVersioning
):
    config.format_jinja = "{{- timestamp }}"

    result = template.render_jinja(version, config)

    assert result == "20250401120000"


def test_when_rendering_version_with_individual_parts_then_returns_formatted_version(
    version: Version,
    config: schemas.UvDynamicVersioning,
):
    config.format_jinja = "{{- major }}.{{- minor }}.{{- patch }}"

    result = template.render_jinja(version, config)

    assert result == "1.0.0"


def test_when_rendering_version_with_escaped_branch_then_returns_escaped_branch(
    version: Version,
    config: schemas.UvDynamicVersioning,
):
    version.branch = "feature/new-branch"
    config.format_jinja = "{{- branch_escaped }}"

    result = template.render_jinja(version, config)

    assert result == "featurenewbranch"


def test_when_rendering_version_with_dirty_flag_then_returns_dirty_status(
    version: Version, config: schemas.UvDynamicVersioning
):
    version.dirty = True
    config.format_jinja = "{{- 'dirty' if dirty else 'clean' }}"

    result = template.render_jinja(version, config)

    assert result == "dirty"


def test_when_rendering_version_with_environment_variables_then_returns_env_value(
    version: Version,
    config: schemas.UvDynamicVersioning,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv("TEST_VAR", "test_value")
    config.format_jinja = "{{ env.TEST_VAR }}"

    result = template.render_jinja(version, config)

    assert result == "test_value"


def test_when_rendering_version_with_serialization_functions_then_returns_serialized_version(
    version: Version,
    config: schemas.UvDynamicVersioning,
):
    config.format_jinja = "{{ serialize_pep440(base, stage, revision) }}"

    result = template.render_jinja(version, config)

    assert result == "1.0.0a1"


def test_when_rendering_version_with_serialization_functions_and_bump_then_returns_bumped_serialized_version(
    version: Version,
    config: schemas.UvDynamicVersioning,
):
    config.format_jinja = "{{ serialize_pep440(bump_version(base), stage, revision) }}"

    result = template.render_jinja(version, config)

    assert result == "1.0.1a1"


def test_when_rendering_version_with_tagged_metadata_then_returns_metadata(
    version: Version,
    config: schemas.UvDynamicVersioning,
):
    version.tagged_metadata = "build123"
    config.format_jinja = "{{ tagged_metadata }}"

    result = template.render_jinja(version, config)

    assert result == "build123"
