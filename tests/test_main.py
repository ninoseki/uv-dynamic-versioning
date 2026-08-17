import os
import subprocess
import sys
from pathlib import Path

import pytest
from dunamai import Style, Version
from git import Repo

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


def test_get_version_with_format_jinja_imports_with_module_only():
    config = schemas.UvDynamicVersioning.from_dict(
        {
            "format-jinja": "{{ math.pow(2, 2) }}",
            "format-jinja-imports": [
                {
                    "module": "math",
                }
            ],
        }
    )
    assert get_version(config)[0] == "4.0"


def test_get_version_with_format_jinja_imports_with_item():
    config = schemas.UvDynamicVersioning.from_dict(
        {
            "format-jinja": "{{ pow(2, 2) }}",
            "format-jinja-imports": [
                {
                    "module": "math",
                    "item": "pow",
                }
            ],
        }
    )
    assert get_version(config)[0] == "4.0"


@pytest.mark.usefixtures("semver_tag")
def test_get_version_with_highest_tag():
    config = schemas.UvDynamicVersioning(highest_tag=True)
    assert get_version(config)[0] == "1.0.0"


@pytest.mark.usefixtures("semver_tag")
def test_get_version_with_highest_tag_selects_highest_version(repo: Repo):
    # Both v1.0.0 (semver_tag) and v0.9.0 point to the same commit.
    # With highest_tag=True the numerically highest tag (v1.0.0) should win.
    low_tag = repo.create_tag("v0.9.0")
    try:
        version_highest = get_version(schemas.UvDynamicVersioning(highest_tag=True))[0]
        assert version_highest.startswith("1.0.0")
    finally:
        repo.delete_tag(low_tag)


# A locale whose encoding cannot represent the non-ASCII fixtures, with both routes
# back to UTF-8 (PEP 540 UTF-8 mode, PEP 538 C locale coercion) disabled. Used to run
# a child interpreter, because the encoding `open` defaults to is fixed at start-up.
NON_UTF8_LOCALE_ENV = {
    **os.environ,
    "LC_ALL": "C",
    "PYTHONUTF8": "0",
    "PYTHONCOERCECLOCALE": "0",
    # Only affects stdio, so the child can hand the decoded text back intact.
    "PYTHONIOENCODING": "utf-8",
}


def test_read_decodes_utf8_regardless_of_locale():
    # `pyproject.toml` is a TOML document, which is UTF-8 by spec, so `read` must not
    # decode it with the locale encoding: on a non-UTF-8 locale that either raises
    # (`UnicodeDecodeError` under `LC_ALL=C` or a Chinese Windows locale) or silently
    # mojibakes the document.
    root = "tests/fixtures/with-non-ascii"
    expected = (Path(root) / "pyproject.toml").read_text(encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; from uv_dynamic_versioning.main import read; "
            f"sys.stdout.write(read({root!r}))",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=NON_UTF8_LOCALE_ENV,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == expected


def test_from_file_decodes_utf8_regardless_of_locale():
    # Same as above for the `from-file` source: with a `pattern` it is meant to be
    # pointed at a source file, whose surrounding content can be non-ASCII.
    root = "tests/fixtures/with-from-file-non-ascii"
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; from uv_dynamic_versioning.base import BasePlugin; "
            "from uv_dynamic_versioning.main import get_version; "
            f"plugin = BasePlugin(); plugin.root = {root!r}; "
            "sys.stdout.write(get_version(plugin.project_config)[0])",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=NON_UTF8_LOCALE_ENV,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "0.0.0"
