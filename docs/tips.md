# Tips

## Dpendabot

Dependabot may fail if your project uses Depandabot and `uv-dynamic-versioning` together.

```yml
version: 2
updates:
  - package-ecosystem: uv
```

This is because Dependabot does `uv lock --upgrade-package {package_name}` and it invokes a build. The build fails with the following RuntimeError:

```text
RuntimeError: Error getting the version from source
`uv-dynamic-versioning`: This does not appear to be a Git project
```

A workaround is setting `fallback-version` in the configuration:

```toml
[tool.uv-dynamic-versioning]
fallback-version = "0.0.0"
```
