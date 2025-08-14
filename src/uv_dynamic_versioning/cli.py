from __future__ import annotations

from .version_source import DynamicVersionSource


def show():
    source = DynamicVersionSource(root=".", config={})
    print(source.get_version_data()["version"])  # noqa: T201


def main() -> None:
    show()
