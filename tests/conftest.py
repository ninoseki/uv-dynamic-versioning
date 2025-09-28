from pathlib import Path

import pytest
from git import Repo

PROJECT_ROOT = Path().resolve()


@pytest.fixture(scope="session")
def repo():
    return Repo.init()


@pytest.fixture(scope="session", autouse=True)
def clear_tags(repo: Repo):
    saved_tags = {tag.name: tag.commit.hexsha for tag in repo.tags}

    for tag in repo.tags:
        repo.delete_tag(tag)

    yield

    for name, ref in saved_tags.items():
        repo.create_tag(name, ref)


@pytest.fixture
def semver_tag(repo: Repo):
    tag = repo.create_tag("v1.0.0")
    try:
        yield tag
    finally:
        repo.delete_tag(tag)
