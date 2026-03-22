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

## Build Caching and Editable Installs

The `uv` cache is aggressive, and needs to be made aware that the project's metadata is dynamic, for example like this:

```toml
[tool.uv]
cache-keys = [{ file = "pyproject.toml" }, { git = { commit = true, tags = true }}]
```

See [`uv`'s docs on dynamic metadata](https://docs.astral.sh/uv/concepts/cache/#dynamic-metadata) for more information.

## Nix (and Other Sandboxed Build Environments)

Nix and similar sandboxed build environments do not provide access to the `.git` directory during builds. Since `uv sync` installs your project as an editable package, it invokes the build backend (hatch + `uv-dynamic-versioning`), which will fail without a Git repository:

```text
RuntimeError: Error getting the version from source
`uv-dynamic-versioning`: This does not appear to be a Git project
```

Note that this affects `uv sync` as well as `uv build` — any command that triggers a build of your project will hit this error.

A workaround is to resolve the version before entering the sandbox and patch `fallback-version` in `pyproject.toml`:

```bash
# Outside of the sandbox (where .git is available):
VERSION=$(uvx uv-dynamic-versioning)
# Linux (GNU sed):
sed -i "s|^fallback-version = \".*\"|fallback-version = \"$VERSION\"|" pyproject.toml
# macOS (BSD sed):
sed -i '' "s|^fallback-version = \".*\"|fallback-version = \"$VERSION\"|" pyproject.toml
```

This requires a `fallback-version` entry to already exist in your configuration:

```toml
[tool.uv-dynamic-versioning]
fallback-version = "0.0.0"
```

Inside the sandbox, `uv sync`/`build` will then use the patched `fallback-version` instead of querying Git.
