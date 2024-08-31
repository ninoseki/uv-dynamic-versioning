from hatchling.plugin import hookimpl

from .version_source import DynamicVersionSource


@hookimpl
def hatch_register_version_source():
    return DynamicVersionSource
