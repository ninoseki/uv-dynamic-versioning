from .version_source import DynamicVersionSource


def main() -> None:
    source = DynamicVersionSource(root=".", config={})
    print(source.get_version_data()["version"])  # noqa: T201
