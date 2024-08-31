from uv_dynamic_versioning import schemas
from uv_dynamic_versioning.main import get_version


def test_get_version():
    version = get_version(schemas.UvDynamicVersioning()).unwrap()
    assert version != ""
