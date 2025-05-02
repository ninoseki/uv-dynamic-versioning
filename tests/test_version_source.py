import os
from collections.abc import Generator
from unittest.mock import PropertyMock, patch

import pytest
from dunamai import Style, Version
from git import Repo, TagReference

from uv_dynamic_versioning import schemas
from uv_dynamic_versioning.version_source import DynamicVersionSource, get_version


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


@pytest.mark.usefixtures("set_uv_dynamic_versioning_bypass")
def test_get_version_with_bypass(version: str):
    assert get_version(schemas.UvDynamicVersioning()) == (
        version,
        Version.parse(version),
    )


@pytest.mark.usefixtures("set_uv_dynamic_versioning_bypass")
def test_get_version_with_bypass_with_format(version: str):
    # NOTE: format should be ignored when bypassing
    assert get_version(
        schemas.UvDynamicVersioning(format="v{base}+{distance}.{commit}")
    ) == (
        version,
        Version.parse(version),
    )


@pytest.mark.usefixtures("semver_tag")
def test_get_version_with_invalid_combination_of_format_jinja_and_style():
    config = schemas.UvDynamicVersioning.model_validate(
        {
            "format-jinja": "invalid",
            "style": "pep440",
        }
    )
    assert config.style == Style.Pep440
    with pytest.raises(ValueError):
        get_version(config)
