import pytest
from git import TagReference

from uv_dynamic_versioning.build_hook import DynamicBuildHook


def test_with_template(semver_tag: TagReference):
    config = {"template": "__version__ = {version!r}"}
    hook = DynamicBuildHook(
        str(semver_tag.repo.working_dir),
        config,
        None,
        None,  # type: ignore
        str(semver_tag.repo.working_dir),
        "wheel",
    )
    assert hook.config_template == "__version__ = {version!r}"


def test_with_invalid_template(semver_tag: TagReference):
    config = {"template": 0}
    hook = DynamicBuildHook(
        str(semver_tag.repo.working_dir),
        config,
        None,
        None,  # type: ignore
        str(semver_tag.repo.working_dir),
        "wheel",
    )
    with pytest.raises(TypeError):
        assert hook.config_template
