import pytest
from dunamai import Style, Version

from uv_dynamic_versioning import schemas
from uv_dynamic_versioning.main import get_version


@pytest.mark.usefixtures("semver_tag")
def test_get_version_with_semver_tag():
    config = schemas.UvDynamicVersioning()
    assert get_version(config)[0] == "1.0.0"


@pytest.mark.usefixtures("prerelease_tag")
def test_get_version_with_prerelease_tag():
    config = schemas.UvDynamicVersioning()
    assert get_version(config)[0] == "1.0.0a1"


@pytest.mark.usefixtures("dev_tag")
def test_get_version_with_dev_tag():
    config = schemas.UvDynamicVersioning()
    assert get_version(config)[0] == "1.0.0.dev1"


def test_get_version_with_bump():
    version_without_bump = get_version(schemas.UvDynamicVersioning())
    version_with_bump = get_version(schemas.UvDynamicVersioning(bump=True))
    # bumped version should be greater than non-bumped version
    assert Version(version_with_bump[0]) > Version(version_without_bump[0])


def test_get_version_with_bypass(uv_dynamic_versioning_bypass_with_semver_tag: str):
    assert get_version(schemas.UvDynamicVersioning()) == (
        uv_dynamic_versioning_bypass_with_semver_tag,
        Version.parse(uv_dynamic_versioning_bypass_with_semver_tag),
    )


def test_get_version_with_bypass_with_format(
    uv_dynamic_versioning_bypass_with_semver_tag: str,
):
    # NOTE: format should be ignored when bypassing
    assert get_version(
        schemas.UvDynamicVersioning(format="v{base}+{distance}.{commit}")
    ) == (
        uv_dynamic_versioning_bypass_with_semver_tag,
        Version.parse(uv_dynamic_versioning_bypass_with_semver_tag),
    )


@pytest.mark.usefixtures("semver_tag")
def test_get_version_with_invalid_combination_of_format_jinja_and_style():
    config = schemas.UvDynamicVersioning.from_dict(
        {
            "format-jinja": "invalid",
            "style": "pep440",
        }
    )
    assert config.style == Style.Pep440
    with pytest.raises(ValueError):
        get_version(config)
