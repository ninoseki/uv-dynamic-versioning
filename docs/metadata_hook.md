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

- `dependencies`: is a list of Jinja2 templates. `dependencies` should be set in `project.dynamic`. Available variables:
  - `version`: Version ([dunamai.version](https://dunamai.readthedocs.io/en/latest/#dunamai.Version))
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
- `optional-dependencies`: is an optional dependencies and each dependency is a list of Jinaj2 templates. `optional-dependencies` should be set in `project.dynamic`. Available variables are same as the above.
