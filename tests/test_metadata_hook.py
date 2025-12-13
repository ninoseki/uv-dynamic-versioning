from collections.abc import Generator
from unittest.mock import PropertyMock, patch

import pytest
from git import Repo, TagReference

from uv_dynamic_versioning.metadata_hook import DependenciesMetadataHook

from .utils import dirty


def test_without_dynamic_dependencies(semver_tag: TagReference):
    hook = DependenciesMetadataHook(str(semver_tag.repo.working_dir), {})

    with pytest.raises(ValueError):
        hook.update({})


@pytest.fixture
def mock_config() -> Generator[PropertyMock, None, None]:
    with patch(
        "uv_dynamic_versioning.metadata_hook.DependenciesMetadataHook.config",
        new_callable=PropertyMock,
    ) as mock:
        yield mock


@pytest.fixture
def mock_root() -> Generator[PropertyMock, None, None]:
    with patch(
        "uv_dynamic_versioning.metadata_hook.DependenciesMetadataHook.root",
        new_callable=PropertyMock,
    ) as mock:
        yield mock


def test_without_dependencies_in_config(
    semver_tag: TagReference, mock_config: PropertyMock
):
    mock_config.return_value = {}
    hook = DependenciesMetadataHook(str(semver_tag.repo.working_dir), {})
    with pytest.raises(ValueError):
        hook.update(
            {
                "dynamic": ["dependencies"],
            }
        )


def test_render_dependencies_with_semver(
    semver_tag: TagReference, mock_config: PropertyMock
):
    mock_config.return_value = {
        "dependencies": ["foo=={{ version }}"],
    }

    hook = DependenciesMetadataHook(str(semver_tag.repo.working_dir), {})

    assert hook.render_dependencies() == ["foo==1.0.0"]
    assert (
        hook.update(
            {
                "dynamic": ["dependencies"],
            }
        )
        is None
    )


def test_render_dependencies_with_dirty(
    semver_tag: TagReference,
    mock_config: PropertyMock,
    mock_root: PropertyMock,
    repo: Repo,
):
    mock_config.return_value = {
        "dependencies": ["foo=={{ version }}"],
    }

    mock_root.return_value = "tests/fixtures/with-dirty/"

    hook = DependenciesMetadataHook(str(semver_tag.repo.working_dir), {})

    with dirty(repo):
        dependencies = hook.render_dependencies() or []

    assert len(dependencies) == 1
    assert dependencies[0].endswith("+dirty")


def test_render_dependencies_with_prerelease_tag(
    prerelease_tag: TagReference,
    mock_config: PropertyMock,
):
    mock_config.return_value = {
        "dependencies": ["foo=={{ version }}"],
    }

    hook = DependenciesMetadataHook(str(prerelease_tag.repo.working_dir), {})

    dependencies = hook.render_dependencies() or []

    assert len(dependencies) == 1
    assert dependencies[0].endswith("a1")


def test_render_dependencies_with_bypass_with_semver_tag(
    semver_tag: TagReference,
    mock_config: PropertyMock,
):
    mock_config.return_value = {
        "dependencies": ["foo=={{ version }}"],
    }

    hook = DependenciesMetadataHook(str(semver_tag.repo.working_dir), {})

    dependencies = hook.render_dependencies() or []

    assert len(dependencies) == 1
    assert dependencies[0] == "foo==1.0.0"


def test_render_dependencies_with_bypass_and_prerelease_tag(
    prerelease_tag: TagReference,
    mock_config: PropertyMock,
):
    mock_config.return_value = {
        "dependencies": ["foo=={{ version }}"],
    }

    hook = DependenciesMetadataHook(str(prerelease_tag.repo.working_dir), {})

    dependencies = hook.render_dependencies() or []

    assert len(dependencies) == 1
    assert dependencies[0] == "foo==1.0.0a1"


def test_render_dependencies_with_bypass_and_dev_tag(
    dev_tag: TagReference,
    mock_config: PropertyMock,
):
    mock_config.return_value = {
        "dependencies": ["foo=={{ version }}"],
    }

    hook = DependenciesMetadataHook(str(dev_tag.repo.working_dir), {})

    dependencies = hook.render_dependencies() or []

    assert len(dependencies) == 1
    assert dependencies[0] == "foo==1.0.0.dev1"
