import os
from collections.abc import Generator
from unittest.mock import PropertyMock, patch

import pytest
from dunamai import Version
from git import Repo, TagReference

from uv_dynamic_versioning import schemas
from uv_dynamic_versioning.main import get_version
from uv_dynamic_versioning.version_source import DynamicVersionSource


@pytest.fixture
def mock_root() -> Generator[PropertyMock, None, None]:
    with patch(
        "uv_dynamic_versioning.version_source.DynamicVersionSource.root",
        new_callable=PropertyMock,
    ) as mock:
        yield mock


@pytest.fixture
def version():
    return "1.1.1"


@pytest.fixture
def set_uv_dynamic_versioning_bypass(version: str):
    os.environ["UV_DYNAMIC_VERSIONING_BYPASS"] = version

    try:
        yield version
    finally:
        del os.environ["UV_DYNAMIC_VERSIONING_BYPASS"]


@pytest.fixture
def set_uv_dynamic_versioning_bypass_empty(version: str):
    os.environ["UV_DYNAMIC_VERSIONING_BYPASS"] = ""

    try:
        yield ""
    finally:
        del os.environ["UV_DYNAMIC_VERSIONING_BYPASS"]


@pytest.mark.usefixtures("set_uv_dynamic_versioning_bypass")
def test_get_version(version: str):
    assert get_version(schemas.UvDynamicVersioning()) == (
        version,
        Version.parse(version),
    )


@pytest.mark.usefixtures("set_uv_dynamic_versioning_bypass")
def test_get_version_with_smart_bump(version: str):
    """Test UV_DYNAMIC_VERSIONING_BYPASS with "smart" version bump enabled"""
    assert get_version(
        schemas.UvDynamicVersioning(bump=schemas.BumpConfig(enable=True, smart=True))
    ) == (
        version,
        Version.parse(version),
    )


@pytest.mark.usefixtures("set_uv_dynamic_versioning_bypass")
def test_with_bump_and_bypass(
    repo: Repo, semver_tag: TagReference, mock_root: PropertyMock
):
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})
    mock_root.return_value = "tests/fixtures/with-bump/"
    repo.git.execute(
        ["git", "commit", "--allow-empty", "-m", "empty commit", "--no-gpg-sign"]
    )

    try:
        internal_version: str = source.get_version_data()["version"]
        assert internal_version.startswith("1.1.1")
    finally:
        repo.git.execute(["git", "reset", "--soft", "HEAD~1"])


@pytest.mark.usefixtures("set_uv_dynamic_versioning_bypass")
def test_get_version_with_bump_and_bypass(version: str):
    """Test UV_DYNAMIC_VERSIONING_BYPASS with guaranteed version bump (not "smart") enabled"""
    assert get_version(
        schemas.UvDynamicVersioning(bump=schemas.BumpConfig(enable=True, smart=False))
    ) == (
        version,
        Version.parse(version),
    )


@pytest.mark.usefixtures("set_uv_dynamic_versioning_bypass_empty")
def test_get_version_with_empty_string_for_bypass(
    repo: Repo, semver_tag: TagReference, mock_root: PropertyMock, version: str
):
    """Verify that UV_DYNAMIC_VERSIONING_BYPASS='' (empty string) is treated as unset and executes get_version() as
    normal.
    """
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})
    mock_root.return_value = "tests/fixtures/with-bump/"

    assert "UV_DYNAMIC_VERSIONING_BYPASS" in os.environ

    repo.git.execute(
        ["git", "commit", "--allow-empty", "-m", "empty commit", "--no-gpg-sign"]
    )

    try:
        internal_version: str = source.get_version_data()["version"]
        assert internal_version.startswith("1.0.1")
    finally:
        repo.git.execute(["git", "reset", "--soft", "HEAD~1"])
