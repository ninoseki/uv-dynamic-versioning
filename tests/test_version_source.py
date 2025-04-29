from collections.abc import Generator
from unittest.mock import PropertyMock, patch

import pytest
from git import Repo, TagReference

from uv_dynamic_versioning.version_source import DynamicVersionSource


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
