# uv-dynamic-versioning

[poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning) influenced dynamic versioning tool for [uv](https://github.com/astral-sh/uv)/[hatch](https://github.com/pypa/hatch), powered by [dunamai](https://github.com/mtkennerly/dunamai/).

## Installation

Update or add `build-system` to use `uv-dynamic-versioning`.

```toml
[build-system]
requires = ["hatchling", "uv-dynamic-versioning"]
build-backend = "hatchling.build"
```

## Plugins

This project offers two plugins:

- Version source plugin: is for setting a version based on VCS.
- Metadata hook plugin: is for setting dependencies and optional-dependencies dynamically based on on VCS. This plugin is useful for monorepo.

See [Version Source](docs/version_source.md) and [Metadata Hook](docs/metadata_hook.md) for more details.

## Examples

See [Examples](./examples/).

## Alternatives

- [hatch-vcs](https://github.com/ofek/hatch-vcs): Hatch plugin for versioning with your preferred VCS.
- [versioningit](https://github.com/jwodder/versioningit): Versioning It with your Version In Git.
