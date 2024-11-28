import os

import pytest

from uv_dynamic_versioning import schemas
from uv_dynamic_versioning.main import get_version


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
def test_get_version(version: str):
    got = get_version(schemas.UvDynamicVersioning()).unwrap()
    assert got == version
