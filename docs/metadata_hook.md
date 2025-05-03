# Metadata Hook

`uv-dynamic-versioning` metadata hook allows you to set `dependencies` and `optional-dependencies` dynamically with a VCS based version.

> [!NOTE]
> VCS based version configuration is the same as described at [Version Source](./version_source.md).

Add `[tool.hatch.metadata.hooks.uv-dynamic-versioning]` in your `pyproject.toml` to use it.

```toml
[tool.hatch.metadata.hooks.uv-dynamic-versioning]
dependencies = ["foo=={{ version }}"]
```

Also remove `dependencies` in `project` and set them in `project.dynamic` (`dynamic = ["dependencies"]`).

**Before**

```toml
[project]
name = "..."
dependencies = []
```

**After**

```toml
[project]
name = "..."
dynamic = ["dependencies"]
```

`optional-dependencies` can be set in the same way.

## Configuration

- `dependencies`: is a list of Jinja2 templates. `dependencies` should be set in `project.dynamic`.

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

- `optional-dependencies`: is an optional dependencies and each dependency is a list of Jinja2 templates. `optional-dependencies` should be set in `project.dynamic`. Available variables are same as the above.
