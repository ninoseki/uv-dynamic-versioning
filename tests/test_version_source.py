import os
from collections.abc import Generator
from unittest.mock import PropertyMock, patch

import pytest
from git import Repo, TagReference

from uv_dynamic_versioning.version_source import DynamicVersionSource


@pytest.fixture
def bypass_version():
    return "2.3.4"


@pytest.fixture
def set_uv_dynamic_versioning_bypass(bypass_version: str):
    os.environ["UV_DYNAMIC_VERSIONING_BYPASS"] = bypass_version

    try:
        yield bypass_version
    finally:
        del os.environ["UV_DYNAMIC_VERSIONING_BYPASS"]


@pytest.fixture
def mock_root() -> Generator[PropertyMock, None, None]:
    with patch(
        "uv_dynamic_versioning.version_source.DynamicVersionSource.root",
        new_callable=PropertyMock,
    ) as mock:
        yield mock


def test_with_semver(semver_tag: TagReference, mock_root: PropertyMock):
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})
    mock_root.return_value = "tests/fixtures/with-semver/"

    version = source.get_version_data()["version"]
    assert version == "1.0.0"


def test_with_format(semver_tag: TagReference, mock_root: PropertyMock):
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})
    mock_root.return_value = "tests/fixtures/with-format/"

    version: str = source.get_version_data()["version"]
    assert version.startswith("v1.0.0+")


def test_with_bump(repo: Repo, semver_tag: TagReference, mock_root: PropertyMock):
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})
    mock_root.return_value = "tests/fixtures/with-bump/"
    repo.git.execute(["git", "commit", "--allow-empty", "-m", "empty commit"])

    try:
        version: str = source.get_version_data()["version"]
        assert version.startswith("1.0.1.")
    finally:
        repo.git.execute(["git", "reset", "--soft", "HEAD~1"])


def test_with_jinja2_format(semver_tag: TagReference, mock_root: PropertyMock):
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})
    mock_root.return_value = "tests/fixtures/with-jinja-format/"

    version: str = source.get_version_data()["version"]
    assert version.startswith("1.0.0.dev0+g")


def test_with_pattern(semver_tag: TagReference, mock_root: PropertyMock):
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})
    mock_root.return_value = "tests/fixtures/with-pattern/"

    version: str = source.get_version_data()["version"]
    assert version == "1"


@pytest.mark.usefixtures("set_uv_dynamic_versioning_bypass")
def test_with_bump_and_bypass(
    semver_tag: TagReference, mock_root: PropertyMock, bypass_version: str
):
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})
    mock_root.return_value = "tests/fixtures/with-bump-and-format/"
    semver_tag.repo.git.execute(
        ["git", "commit", "--allow-empty", "-m", "empty commit", "--no-gpg-sign"]
    )

    assert "UV_DYNAMIC_VERSIONING_BYPASS" in os.environ
    assert os.environ["UV_DYNAMIC_VERSIONING_BYPASS"] == bypass_version

    try:
        version: str = source.get_version_data()["version"]
        assert version == bypass_version
    finally:
        semver_tag.repo.git.execute(["git", "reset", "--soft", "HEAD~1"])
