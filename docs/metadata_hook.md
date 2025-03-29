# Metadata Hook

`uv-dynamic-versioning` metadata hook allows you to set `dependencies` and `optional-dependencies` dynamically with a VCS based version.

> [!NOTE]
> VCS based version configuration is the same as described at [Version Source](./version_source.md).

Add `tool.hatch.metadata.hooks.uv-dynamic-versioning` in your `pyproject.toml` to use it.

```toml
[tool.hatch.metadata.hooks.uv-dynamic-versioning]
dependencies = ["foo=={{ version }}"]
optional-dependencies = {
  "bar": ["baz=={{ version }}"]
}
```

Also remove `dependencies` and `optional-dependencies` in `project` and set them in `dynamic` (`dynamic = ["dependencies", "optional-dependencies"]`).

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

## Configuration

- `dependencies` is a list of Jinja2 templates and `version` (a VCS based version as [packaging.version.Version](https://packaging.pypa.io/en/latest/version.html#packaging.version.Version)). `dependencies` should be set in `project.dynamic`.
- `optional-dependencies`: is an optional dependencies and each dependency is a list of Jinaj2 templates (same as the above). `optional-dependencies` should be set in `project.dynamic`.
