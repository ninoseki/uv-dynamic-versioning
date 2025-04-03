from unittest.mock import PropertyMock, patch

import pytest
from git import TagReference

from uv_dynamic_versioning.metadata_hook import DependenciesMetadataHook


def test_without_dynamic_dependencies(semver_tag: TagReference):
    hook = DependenciesMetadataHook(str(semver_tag.repo.working_dir), {})

    with pytest.raises(ValueError):
        hook.update({})


def test_without_dependencies_in_config(semver_tag: TagReference):
    with patch(
        "uv_dynamic_versioning.metadata_hook.DependenciesMetadataHook.config",
        new_callable=PropertyMock,
    ) as mock_root:
        mock_root.return_value = {}

        hook = DependenciesMetadataHook(str(semver_tag.repo.working_dir), {})
        with pytest.raises(ValueError):
            hook.update(
                {
                    "dynamic": ["dependencies"],
                }
            )


def test_foo(semver_tag: TagReference):
    with patch(
        "uv_dynamic_versioning.metadata_hook.DependenciesMetadataHook.config",
        new_callable=PropertyMock,
    ) as mock_root:
        mock_root.return_value = {
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
