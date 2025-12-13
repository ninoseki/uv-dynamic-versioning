import os
from pathlib import Path

import pytest
from git import Repo, TagReference

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


@pytest.fixture
def prerelease_tag(repo: Repo):
    tag = repo.create_tag("v1.0.0-alpha1")
    try:
        yield tag
    finally:
        repo.delete_tag(tag)


@pytest.fixture
def dev_tag(repo: Repo):
    tag = repo.create_tag("v1.0.0-dev1")
    try:
        yield tag
    finally:
        repo.delete_tag(tag)


@pytest.fixture
def uv_dynamic_versioning_bypass_with_semver_tag(
    semver_tag: TagReference,
):
    os.environ["UV_DYNAMIC_VERSIONING_BYPASS"] = semver_tag.name

    try:
        yield semver_tag.name
    finally:
        del os.environ["UV_DYNAMIC_VERSIONING_BYPASS"]


@pytest.fixture
def uv_dynamic_versioning_bypass_with_prerelease_tag(prerelease_tag: TagReference):
    os.environ["UV_DYNAMIC_VERSIONING_BYPASS"] = prerelease_tag.name

    try:
        yield prerelease_tag.name
    finally:
        del os.environ["UV_DYNAMIC_VERSIONING_BYPASS"]


@pytest.fixture
def uv_dynamic_versioning_bypass_with_dev_tag(dev_tag: TagReference):
    os.environ["UV_DYNAMIC_VERSIONING_BYPASS"] = dev_tag.name

    try:
        yield dev_tag.name
    finally:
        del os.environ["UV_DYNAMIC_VERSIONING_BYPASS"]
