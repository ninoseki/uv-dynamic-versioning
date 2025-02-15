from unittest.mock import PropertyMock, patch

from git import Repo, TagReference

from uv_dynamic_versioning.version_source import DynamicVersionSource


def test_with_semver(semver_tag: TagReference):
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})

    with patch(
        "uv_dynamic_versioning.version_source.DynamicVersionSource.root",
        new_callable=PropertyMock,
    ) as mock_root:
        mock_root.return_value = "tests/fixtures/with-semver/"

        version = source.get_version_data()["version"]
        assert version == "1.0.0"


def test_with_format(semver_tag: TagReference):
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})

    with patch(
        "uv_dynamic_versioning.version_source.DynamicVersionSource.root",
        new_callable=PropertyMock,
    ) as mock_root:
        mock_root.return_value = "tests/fixtures/with-format/"

        version: str = source.get_version_data()["version"]
        assert version.startswith("v1.0.0+")


def test_with_bump(repo: Repo, semver_tag: TagReference):
    source = DynamicVersionSource(str(semver_tag.repo.working_dir), {})

    repo.git.execute(["git", "commit", "--allow-empty", "-m", "empty commit"])
    try:
        with patch(
            "uv_dynamic_versioning.version_source.DynamicVersionSource.root",
            new_callable=PropertyMock,
        ) as mock_root:
            mock_root.return_value = "tests/fixtures/with-bump/"

            version: str = source.get_version_data()["version"]
            assert version.startswith("1.0.1.")
    finally:
        repo.git.execute(["git", "reset", "--soft", "HEAD~1"])
