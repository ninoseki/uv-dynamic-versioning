from __future__ import annotations

from functools import cached_property

from hatchling.metadata.plugin.interface import MetadataHookInterface
from jinja2 import Environment
from packaging.version import Version
from returns.pipeline import flow

from . import schemas
from .main import get_version, parse, read, validate


def render_template(s: str, *, env: Environment, version: Version):
    template = env.from_string(s)
    return template.render(version=version)


class DependenciesMetadataHook(MetadataHookInterface):
    """
    Hatch metadata hook to populate `project.dependencies` and `project.optional-dependencies`
    """

    PLUGIN_NAME = "uv-dynamic-versioning"

    @cached_property
    def project(self) -> schemas.Project:
        return flow(read(self.root), parse, validate)

    @property
    def project_config(self) -> schemas.UvDynamicVersioning:
        return self.project.tool.uv_dynamic_versioning or schemas.UvDynamicVersioning()

    @cached_property
    def plugin_config(self) -> schemas.MetadataHookConfig:
        return schemas.MetadataHookConfig.model_validate(self.config)

    def update(self, metadata: dict) -> None:
        # check dynamic
        dynamic = metadata.get("dynamic", [])
        is_dynamic_dependencies = "dependencies" in dynamic
        is_dynamic_optional_dependencies = "optional-dependencies" in dynamic
        if not (is_dynamic_dependencies or is_dynamic_optional_dependencies):
            raise ValueError(
                "Cannot use this plugin when 'dependencies' or 'optional-dependencies' is not listed in 'project.dynamic'."
            )

        # check consistency between dynamic and project
        has_dependencies = "dependencies" in metadata
        has_optional_dependencies = "optional-dependencies" in metadata
        if is_dynamic_dependencies and has_dependencies:
            raise ValueError(
                "'dependencies' is dynamic but already listed in [project]."
            )

        if is_dynamic_optional_dependencies and has_optional_dependencies:
            raise ValueError(
                "'optional-dependencies' is dynamic but already listed in [project]."
            )

        has_dependencies = self.plugin_config.dependencies is not None
        has_optional_dependencies = self.plugin_config.optional_dependencies is not None
        if not has_dependencies and not has_optional_dependencies:
            raise ValueError(
                "No dependencies or optional-dependencies found in the plugin config."
            )

        env = Environment()
        _version = get_version(self.project_config)
        version = Version(_version)

        if self.plugin_config.dependencies:
            dependencies = [
                render_template(dep, env=env, version=version)
                for dep in self.plugin_config.dependencies
            ]
            metadata["dependencies"] = dependencies

        if self.plugin_config.optional_dependencies:
            optional_dependencies = {
                name: [render_template(dep, env=env, version=version) for dep in deps]
                for name, deps in self.plugin_config.optional_dependencies.items()
            }
            metadata["optional-dependencies"] = optional_dependencies
