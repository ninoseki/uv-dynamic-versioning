# Version Source

`uv-dynamic-versioning` version source allows you to set a version based on VCS.

Add `tool.hatch.version` in your `pyproject.toml` to use it.

```toml
[tool.hatch.version]
source = "uv-dynamic-versioning"
```

Also remove `version` in `project` and set it in `project.dynamic` (`dynamic = ["version"]`).

**Before**

```toml
[project]
name = "..."
version = "0.1.0"
```

**After**

```toml
[project]
name = "..."
dynamic = ["version"]
```

## Configuration

> [!NOTE]
>
> - Configuration is almost same to [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning). But `format-jinja-imports` is not supported.
> - The following descriptions are excerpts from [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning).

In your `pyproject.toml`, you may configure the following options:

- `[tool.uv-dynamic-versioning]`:
  General options.

  - `vcs` (string, default: `any`):
    This is the version control system to check for a version.
    One of: `any`, `git`, `mercurial`, `darcs`, `bazaar`, `subversion`, `fossil`, `pijul`.
  - `metadata` (boolean, default: unset):
    If true, include the commit hash in the version,
    and also include a dirty flag if `dirty` is true.
    If unset, metadata will only be included if you are on a commit without a version tag.
    This is ignored when `format` or `format-jinja` is used.
  - `tagged-metadata` (boolean, default: false):
    If true, include any tagged metadata discovered as the first part of the metadata segment.
    Has no effect when `metadata` is set to false.
    This is ignored when `format` or `format-jinja` is used.
  - `dirty` (boolean, default: false):
    If true, include a dirty flag in the metadata,
    indicating whether there are any uncommitted changes.
    Has no effect when `metadata` is set to false.
    This is ignored when `format` or `format-jinja` is used.
  - `pattern` (string):
    This is a regular expression which will be used to find a tag representing a version.
    When this is unset, Dunamai's default pattern is used.

    There must be a capture group named `base` with the main part of the version.
    Optionally, it may contain another two groups named `stage` and `revision` for prereleases,
    and it may contain a group named `tagged_metadata` to be used with the `tagged-metadata` option.
    There may also be a group named `epoch` for the PEP 440 concept.

    If the `base` group is not included,
    then this will be interpreted as a named preset from the Dunamai `Pattern` class.
    This includes: `default`, `default-unprefixed` (makes the `v` prefix optional).

    You can check the default for your installed version of Dunamai by running this command:

    ```bash
    poetry run python -c "import dunamai; print(dunamai.Pattern.Default.regex())"
    ```

    Remember that backslashes must be escaped in the TOML file.

    ```toml
    # Regular expression:
    pattern = '(?P<base>\d+\.\d+\.\d+)'
    # Named preset:
    pattern = "default-unprefixed"
    ```

  - `pattern-prefix` (string):
    This will be inserted after the pattern's start anchor (`^`).
    For example, to match tags like `some-package-v1.2.3`,
    you can keep the default pattern and set the prefix to `some-package-`.
  - `format` (string, default: unset):
    This defines a custom output format for the version. Available substitutions:

    - `{base}`
    - `{stage}`
    - `{revision}`
    - `{distance}`
    - `{commit}`
    - `{dirty}`
    - `{tagged_metadata}`
    - `{branch}`
    - `{branch_escaped}` which omits any non-letter/number characters
    - `{timestamp}` of the current commit, which expands to YYYYmmddHHMMSS as UTC

    Example: `v{base}+{distance}.{commit}`

  - `format-jinja` (string, default: empty):
    Jinja2 template for version formatting. Available variables:
    - `base`: Base version (e.g., "1.0.0")
    - `stage`: Stage (e.g., "alpha", "beta", "rc")
    - `revision`: Revision number
    - `distance`: Number of commits since last tag
    - `commit`: Commit hash
    - `dirty`: Boolean indicating if working directory is dirty
    - `branch`: Current branch name
    - `tagged_metadata`: Metadata from tag
    - `branch_escaped`: Branch name with special characters removed
    - `timestamp`: Timestamp of the commit
    - `major`: Major version number
    - `minor`: Minor version number
    - `patch`: Patch version number
    - `env`: Environment variables
    - `bump_version`: Function to bump version
    - `serialize_pep440`: Function to serialize version in PEP 440 format
    - `serialize_pvp`: Function to serialize version in PVP format
    - `serialize_semver`: Function to serialize version in SemVer format

  - `style` (string, default: unset):
    One of: `pep440`, `semver`, `pvp`.
    These are preconfigured output formats.
    If you set both a `style` and a `format`,
    then the format will be validated against the style's rules.
    If `style` is unset, the default output format will follow PEP 440,
    but a custom `format` will only be validated if `style` is set explicitly.
  - `latest-tag` (boolean, default: false):
    If true, then only check the latest tag for a version,
    rather than looking through all the tags until a suitable one is found to match the `pattern`.
  - `bump` (boolean, default: false):
    If true, then increment the last part of the version `base` by 1,
    unless the `stage` is set,
    in which case increment the `revision` by 1 or set it to a default of 2 if there was no `revision`.
    Does nothing when on a commit with a version tag.

    Example, if there have been 3 commits since the `v1.3.1` tag:

    - PEP 440 with `bump = false`: `1.3.1.post3.dev0+28c1684`
    - PEP 440 with `bump = true`: `1.3.2.dev3+28c1684`

  - `tag-branch` (string, default: unset):
    Branch on which to find tags, if different than the current branch.
    This is only used for Git currently.
  - `full-commit` (boolean, default: false):
    If true, get the full commit hash instead of the short form.
    This is only used for Git and Mercurial.
  - `strict` (boolean, default: false):
    If true, then fail instead of falling back to 0.0.0 when there are no tags.
  - `ignore-untracked` (boolean, default: false):
    If true, ignore untracked files when determining whether the repository is dirty.

Simple example:

```toml
[tool.uv-dynamic-versioning]
vcs = "git"
style = "semver"
```

## Environment variables

In addition to the project-specific configuration above, you can apply some global overrides via environment variables.

- `UV_DYNAMIC_VERSIONING_BYPASS`:
  Use this to bypass the VCS mechanisms and use a static version instead.
  The value of the environment variable will be used as the version for the active project and any path/SSH dependencies that also use the plugin.
  This is mainly for distro package maintainers who need to patch existing releases, without needing access to the original repository.

# `__version__` Attribute

You may want to set `__version__` attribute in your library. There are two ways for that. Using [importlib.metadata](https://docs.python.org/3/library/importlib.metadata.html) and using [version build hook](https://hatch.pypa.io/1.9/plugins/build-hook/version/).

## `importlib.metadata`

> [!NOTE]
> This is very handy, but it's known that `importlib.metadata` is relatively slow.
> Don't use this method when performance is critical.

```py
# __init__.py
import importlib.metadata

__version__ = importlib.metadata.version(__name__)
```

This trick may fail if a package is installed in [development mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html). Setting a fallback for `importlib.metadata.PackageNotFoundError` may be a good workaround.

```py
import importlib.metadata

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"
```

## Version Build Hook

You can write a version to a file when you run a build by using Hatch's official [version build hook](https://hatch.pypa.io/1.9/plugins/build-hook/version/).

For example:

```toml
[tool.hatch.build.hooks.version]
path = "path/to/_version.py"
template = '''
version = "{version}"
'''
```

> [!NOTE]
> A version file should not be included in VCS. It's better to ignore it in `.gitignore`.
>
> **.gitignore**
>
> ```text
> path/to/_version.py
> ```
