# Tips

## Dependabot

Dependabot may fail if your project uses Depandabot and `uv-dynamic-versioning` together.

```yml
version: 2
updates:
  - package-ecosystem: uv
```

This is because Dependabot does `uv lock --upgrade-package {package_name}` and it invokes a build. The build may fail with the following RuntimeError:

```text
RuntimeError: Error getting the version from source
`uv-dynamic-versioning`: This does not appear to be a Git project
```

A workaround is setting `fallback-version` in the configuration:

```toml
[tool.uv-dynamic-versioning]
fallback-version = "0.0.0"
```

## Build caching and editable installs

The `uv` cache is aggressive, and needs to be made aware that the project's metadata is dynamic, for example like this:

```toml
[tool.uv]
cache-keys = [{ file = "pyproject.toml" }, { git = { commit = true, tags = true }}]
```

See [`uv`'s docs on dynamic metadata](https://docs.astral.sh/uv/concepts/cache/#dynamic-metadata) for more information.
