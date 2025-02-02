from pathlib import Path

import pytest
from git import Repo

PROJECT_ROOT = Path().resolve()


@pytest.fixture
def repo():
    return Repo.init(PROJECT_ROOT)


@pytest.fixture
def semver_tag(repo: Repo):
    tag = repo.create_tag("v1.0.0")
    yield tag
    repo.delete_tag(tag)
