import os

from uv_dynamic_versioning import schemas
from uv_dynamic_versioning.main import get_version


def test_get_version():
    version = "1.1.1"
    os.environ["UV_DYNAMIC_VERSIONING_BYPASS"] = version
    version = get_version(schemas.UvDynamicVersioning()).unwrap()

    assert version == version
