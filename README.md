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
- Metadata hook plugin: is for setting dependencies and optional-dependencies dynamically based on VCS version. This plugin is useful for monorepo.

See [Version Source](docs/version_source.md) and [Metadata Hook](docs/metadata_hook.md) for more details.

## Examples

See [Examples](./examples/).

## Projects Using `uv-dynamic-versioning`

- [microsoft/essex-toolkit](https://github.com/microsoft/essex-toolkit): uses the version source plugin.
- [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk): uses the version source plugin.
- [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai): uses the version source and the metadata hook plugins.

And more.

## Alternatives

- [hatch-vcs](https://github.com/ofek/hatch-vcs): Hatch plugin for versioning with your preferred VCS.
- [versioningit](https://github.com/jwodder/versioningit): Versioning It with your Version In Git.
