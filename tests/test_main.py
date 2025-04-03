import pytest
from packaging.version import Version

from uv_dynamic_versioning import schemas
from uv_dynamic_versioning.main import get_version


@pytest.mark.usefixtures("semver_tag")
def test_get_version():
    config = schemas.UvDynamicVersioning()
    assert get_version(config)[0] == "1.0.0"


def test_get_version_with_bump():
    version_without_bump = get_version(schemas.UvDynamicVersioning())
    version_with_bump = get_version(schemas.UvDynamicVersioning(bump=True))
    # bumped version should be greater than non-bumped version
    assert Version(version_with_bump[0]) > Version(version_without_bump[0])
