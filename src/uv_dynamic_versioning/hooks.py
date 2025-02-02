from hatchling.plugin import hookimpl

from .build_hook import DynamicBuildHook
from .version_source import DynamicVersionSource


@hookimpl
def hatch_register_version_source():
    return DynamicVersionSource


@hookimpl
def hatch_register_build_hook():
    return DynamicBuildHook
