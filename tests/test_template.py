from datetime import datetime, timezone

import pytest
from dunamai import Version

from uv_dynamic_versioning.template import render_template


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


def test_when_rendering_basic_version_then_returns_base_version(version: Version):
    assert render_template("{{- base }}", version=version) == "1.0.0"


def test_when_bumping_version_then_returns_bumped_version(version: Version):
    version.distance = 2
    version.revision = 1
    assert (
        render_template("{{- base }}+r{{- revision }}", version=version) == "1.0.0+r1"
    )


def test_when_rendering_version_with_stage_and_revision_then_returns_formatted_version(
    version: Version,
):
    assert (
        render_template("{{- base }}{{- stage }}{{- revision }}", version=version)
        == "1.0.0alpha1"
    )


def test_when_rendering_version_with_commit_and_branch_then_returns_formatted_version(
    version: Version,
):
    assert (
        render_template("{{- commit }}-{{- branch }}", version=version)
        == "message-main"
    )


def test_when_rendering_version_with_timestamp_then_returns_formatted_timestamp(
    version: Version,
):
    result = render_template("{{- timestamp }}", version=version)
    assert result == "20250401120000"


def test_when_rendering_version_with_individual_parts_then_returns_formatted_version(
    version: Version,
):
    assert (
        render_template("{{- major }}.{{- minor }}.{{- patch }}", version=version)
        == "1.0.0"
    )


def test_when_rendering_version_with_escaped_branch_then_returns_escaped_branch(
    version: Version,
):
    version.branch = "feature/new-branch"
    assert (
        render_template(
            "{{- branch_escaped }}",
            version=version,
        )
        == "featurenewbranch"
    )


def test_when_rendering_version_with_dirty_flag_then_returns_dirty_status(
    version: Version,
):
    version.dirty = True
    assert (
        render_template(
            "{{- 'dirty' if dirty else 'clean' }}",
            version=version,
        )
        == "dirty"
    )


def test_when_rendering_version_with_environment_variables_then_returns_env_value(
    version: Version,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv("TEST_VAR", "test_value")
    assert render_template("{{ env.TEST_VAR }}", version=version) == "test_value"


def test_when_rendering_version_with_serialization_functions_then_returns_serialized_version(
    version: Version,
):
    assert (
        render_template(
            "{{ serialize_pep440(base, stage, revision) }}",
            version=version,
        )
        == "1.0.0a1"
    )


def test_when_rendering_version_with_serialization_functions_and_bump_then_returns_bumped_serialized_version(
    version: Version,
):
    assert (
        render_template(
            "{{ serialize_pep440(bump_version(base), stage, revision) }}",
            version=version,
        )
        == "1.0.1a1"
    )


def test_when_rendering_version_with_tagged_metadata_then_returns_metadata(
    version: Version,
):
    version.tagged_metadata = "build123"
    assert render_template("{{ tagged_metadata }}", version=version) == "build123"
