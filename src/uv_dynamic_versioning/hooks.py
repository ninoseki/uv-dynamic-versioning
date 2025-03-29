from hatchling.plugin import hookimpl

from .metadata_hook import DependenciesMetadataHook
from .version_source import DynamicVersionSource


@hookimpl
def hatch_register_version_source():
    return DynamicVersionSource


@hookimpl
def hatch_register_metadata_hook() -> type[DependenciesMetadataHook]:
    return DependenciesMetadataHook
