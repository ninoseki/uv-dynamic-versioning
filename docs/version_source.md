# Version Source

`uv-dynamic-versioning` version source allows you to set a version based on VCS.

Add `tool.hatch.version` & `build-system` in your `pyproject.toml` and configure them to use `uv-dynamic-versioning`.

```toml
[build-system]
requires = ["hatchling", "uv-dynamic-versioning"]
build-backend = "hatchling.build"
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

Then this plugin works out of the box (defaults to using the semver style).

For example:

```bash
$ git tag v1.0.0
$ uv build
Building source distribution...
Building wheel from source distribution...
Successfully built dist/foo-1.0.0.tar.gz
Successfully built dist/foo-1.0.0-py3-none-any.whl
# check METADATA file (ref. https://packaging.python.org/en/latest/specifications/core-metadata/)
$ tar -xf dist/foo-1.0.0-py3-none-any.whl
$ head foo-1.0.0.dist-info/METADATA
Metadata-Version: 2.4
Name: foo
Version: 1.0.0
```

> [!NOTE]
> You can use `uv-dynamic-versioning` command to check the version to be used:
>
> ```bash
> $ uvx uv-dynamic-versioning
> 1.0.0
> ```

## Configuration

> [!NOTE]
>
> - Configuration is almost same as [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning). But `format-jinja-imports` and `fix-shallow-repository` are not supported.
> - The following descriptions are excerpts from [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning).

You may configure the following options under `[tool.uv-dynamic-versioning]`:

- `vcs` (string, default: `any`): This is the version control system to check for a version. One of: `any`, `git`, `mercurial`, `darcs`, `bazaar`, `subversion`, `fossil`, `pijul`.
- `metadata` (boolean, default: unset): If true, include the commit hash in the version, and also include a dirty flag if `dirty` is true. If unset, metadata will only be included if you are on a commit without a version tag. This is ignored when `format` or `format-jinja` is used.
- `tagged-metadata` (boolean, default: false): If true, include any tagged metadata discovered as the first part of the metadata segment. Has no effect when `metadata` is set to false. This is ignored when `format` or `format-jinja` is used.
- `dirty` (boolean, default: false): If true, include a dirty flag in the metadata, indicating whether there are any uncommitted changes. Has no effect when `metadata` is set to false. This is ignored when `format` or `format-jinja` is used.
- `pattern` (string): This is a regular expression which will be used to find a tag representing a version. When this is unset, Dunamai's default pattern is used.

  There must be a capture group named `base` with the main part of the version. Optionally, it may contain another two groups named `stage` and `revision` for prereleases, and it may contain a group named `tagged_metadata` to be used with the `tagged-metadata` option. There may also be a group named `epoch` for the PEP 440 concept.

  If the `base` group is not included, then this will be interpreted as a named preset from the Dunamai `Pattern` class. This includes: `default`, `default-unprefixed` (makes the `v` prefix optional). You can check the default for your installed version of Dunamai by running this command:

  ```bash
  uv run python -c "import dunamai; print(dunamai.Pattern.Default.regex())"
  ```

  Remember that backslashes must be escaped in the TOML file.

  ```toml
  # Regular expression:
  pattern = '(?P<base>\d+\.\d+\.\d+)'
  # Named preset:
  pattern = "default-unprefixed"
  ```

- `pattern-prefix` (string): This will be inserted after the pattern's start anchor (`^`). For example, to match tags like `some-package-v1.2.3`, you can keep the default pattern and set the prefix to `some-package-`.
- `format` (string, default: unset): This defines a custom output format for the version. Available substitutions:
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

- `format-jinja` (string, default: unset):
  This defines a custom output format for the version, using a [Jinja](https://pypi.org/project/Jinja2) template. When this is set, `format` is ignored.

  Available variables:
  - `version`([dunamai.version](https://dunamai.readthedocs.io/en/latest/#dunamai.Version))
  - `base` (string)
  - `stage` (string or None)
  - `revision` (integer or None)
  - `distance` (integer)
  - `commit` (string)
  - `dirty` (boolean)
  - `tagged_metadata` (string or None)
  - `version` (dunumai.Version)
  - `env` (dictionary of environment variables)
  - `branch` (string or None)
  - `branch_escaped` (string or None)
  - `timestamp` (string or None)
  - `major` (integer)
  - `minor` (integer)
  - `patch` (integer)

  Available functions:
  - `bump_version` ([from Dunamai](https://dunamai.readthedocs.io/en/latest/#dunamai.bump_version))
  - `serialize_pep440` ([from Dunamai](https://dunamai.readthedocs.io/en/latest/#dunamai.serialize_pep440))
  - `serialize_semver` ([from Dunamai](https://dunamai.readthedocs.io/en/latest/#dunamai.serialize_semver))
  - `serialize_pvp` ([from Dunamai](https://dunamai.readthedocs.io/en/latest/#dunamai.serialize_pvp))

  Simple example:

  ```toml
  format-jinja = "{% if distance == 0 %}{{ base }}{% else %}{{ base }}+{{ distance }}.{{ commit }}{% endif %}"
  ```

  Complex example:

  ```toml
  format-jinja = """
      {%- if distance == 0 -%}
          {{ serialize_pep440(base, stage, revision) }}
      {%- elif revision is not none -%}
          {{ serialize_pep440(base, stage, revision + 1, dev=distance, metadata=[commit]) }}
      {%- else -%}
          {{ serialize_pep440(bump_version(base), stage, revision, dev=distance, metadata=[commit]) }}
      {%- endif -%}
  """
  ```

- `format-jinja-imports` (array of tables, default: empty):
  This defines additional things to import and make available to the `format-jinja` template.
  Each table must contain a `module` key and may also contain an `item` key. Consider this example:

  ```toml
  format-jinja-imports = [
      { module = "foo" },
      { module = "bar", item = "baz" },
  ]
  ```

  This is roughly equivalent to:

  ```python
  import foo
  from bar import baz
  ```

  `foo` and `baz` would then become available in the Jinja formatting.

- `style` (string, default: unset): One of: `pep440`, `semver`, `pvp`. These are pre-configured output formats. If you set both a `style` and a `format`, then the format will be validated against the style's rules. If `style` is unset, the default output format will follow PEP 440, but a custom `format` will only be validated if `style` is set explicitly.

  Regardless of the style you choose, the dynamic version is ultimately subject to Hatchling's validation as well, and Hatchling is designed around PEP 440 versions. Hatchling can usually understand SemVer/etc input, but sometimes, Hatchling may reject an otherwise valid version format.

- `latest-tag` (boolean, default: false): If true, then only check the latest tag for a version, rather than looking through all the tags until a suitable one is found to match the `pattern`.
- `bump` (boolean or table, default: false): If enabled, then increment the last part of the version `base` by 1, unless the `stage` is set, in which case increment the `revision` by 1 or set it to a default of 2 if there was no `revision`. Does nothing when on a commit with a version tag. One of:
  - When set to a boolean, true means enable bumping, with other settings as default.
  - When set to a table, these fields are allowed:
    - `enable` (boolean, default: false):
      If true, enable bumping.
    - `index` (integer, default: -1):
      Numerical position to increment in the base.
      This follows Python indexing rules, so positive numbers start from
      the left side and count up from 0, while negative numbers start from
      the right side and count down from -1.

  Example, if there have been 3 commits since the `v1.3.1` tag:
  - PEP 440 with `bump = false`: `1.3.1.post3.dev0+28c1684`
  - PEP 440 with `bump = true`: `1.3.2.dev3+28c1684`

- `tag-branch` (string, default: unset): Branch on which to find tags, if different than the current branch. This is only used for Git currently.
- `full-commit` (boolean, default: false): If true, get the full commit hash instead of the short form.
  This is only used for Git and Mercurial.
- `strict` (boolean, default: false): If true, then fail instead of falling back to 0.0.0 when there are no tags.
- `ignore-untracked` (boolean, default: false): If true, ignore untracked files when determining whether the repository is dirty.
- `commit-length` (integer, default: unset): Use this many characters from the start of the full commit hash.
- `commit-prefix` (string, default: unset): Add this prefix to the commit ID when serializing. This can be helpful when an all-numeric commit would be misinterpreted. For example, "g" is a common prefix for Git commits.
- `escape-with` (string, default: unset): When escaping, replace invalid characters with this substitution. The default is simply to remove invalid characters.
- `fallback-version` (str, default: unset): Version to be used if an error occurs when obtaining the version, for example, there is no `.git/`. If not specified, unsuccessful version obtaining from vcs will raise an error.
- `from-file`:
  This section lets you read the version from a file instead of the VCS.
  - `source` (string):
    If set, read the version from this file.
    It must be a path relative to the location of pyproject.toml.
    By default, the plugin will read the entire content of the file,
    without leading and trailing whitespace.
  - `pattern` (string):
    If set, use this regular expression to extract the version from the file.
    The first capture group must contain the version.

### Examples

Default (no `tool.uv-dynamic-versioning` in `pyproject.toml`):

```bash
$ git tag v1.0.0
$ uv build
Building source distribution...
Building wheel from source distribution...
Successfully built dist/foo-1.0.0.tar.gz
Successfully built dist/foo-1.0.0-py3-none-any.whl
```

With `pattern`:

```toml
[tool.uv-dynamic-versioning]
pattern = "default-unprefixed"
```

```bash
$ git tag 1.0.0
$ uv build
Building source distribution...
Building wheel from source distribution...
Successfully built dist/foo-1.0.0.tar.gz
Successfully built dist/foo-1.0.0-py3-none-any.whl
```

## Environment Variables

In addition to the project-specific configuration above, you can apply some global overrides via environment variables.

- `UV_DYNAMIC_VERSIONING_BYPASS`:
  Use this to bypass the VCS mechanisms and use a static version instead.
  The value of the environment variable will be used as the version for the active project and any path/SSH dependencies that also use the plugin.
  This is mainly for distro package maintainers who need to patch existing releases, without needing access to the original repository.

## `__version__` Attribute

You may want to set `__version__` attribute in your library. There are two ways for that. Using [importlib.metadata](https://docs.python.org/3/library/importlib.metadata.html) and using [version build hook](https://hatch.pypa.io/1.9/plugins/build-hook/version/).

### `importlib.metadata`

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

### Version Build Hook

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
