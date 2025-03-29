# Metadata Hook

`uv-dynamic-versioning` metadata hook allows you to set `dependencies` and `optional-dependencies` dynamically with a VCS based version.

> [!NOTE]
> VCS based version configuration is the same as described at [Version Source](./version_source.md).

Add `tool.hatch.metadata.hooks.uv-dynamic-versioning` in your `pyproject.toml` to use it.

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

- `dependencies` (`tool.hatch.metadata.hooks.uv-dynamic-versioning.dependencies`): is a list of Jinja2 templates. A template has `version` (a VCS based version as [packaging.version.Version](https://packaging.pypa.io/en/latest/version.html#packaging.version.Version)) variable. `dependencies` should be set in `project.dynamic`.
- `optional-dependencies` (`tool.hatch.metadata.hooks.uv-dynamic-versioning.optional-dependencies`): is an optional dependencies and each dependency is a list of Jinaj2 templates (same as the above). `optional-dependencies` should be set in `project.dynamic`.
