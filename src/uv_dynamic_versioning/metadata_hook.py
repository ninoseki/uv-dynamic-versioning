from __future__ import annotations

from functools import cached_property

from hatchling.metadata.plugin.interface import MetadataHookInterface
from jinja2 import Environment
from packaging.version import Version

from . import schemas
from .base import BasePlugin


def render_template(s: str, *, env: Environment, version: Version):
    template = env.from_string(s)
    return template.render(version=version)


class DependenciesMetadataHook(BasePlugin, MetadataHookInterface):
    """
    Hatch metadata hook to populate `project.dependencies` and `project.optional-dependencies`
    """

    PLUGIN_NAME = "uv-dynamic-versioning"

    @cached_property
    def plugin_config(self) -> schemas.MetadataHookConfig:
        return schemas.MetadataHookConfig.model_validate(self.config)

    @cached_property
    def project_version(self) -> Version:
        version = self.get_version()
        return Version(version)

    def render_dependencies(self) -> list[str] | None:
        if self.plugin_config.dependencies is None:
            return None

        env = Environment()
        return [
            render_template(dep, env=env, version=self.project_version)
            for dep in self.plugin_config.dependencies
        ]

    def render_optional_dependencies(self) -> dict[str, list[str]] | None:
        if self.plugin_config.optional_dependencies is None:
            return None

        env = Environment()
        return {
            name: [
                render_template(dep, env=env, version=self.project_version)
                for dep in deps
            ]
            for name, deps in self.plugin_config.optional_dependencies.items()
        }

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
        if is_dynamic_dependencies and has_dependencies:
            raise ValueError(
                "'dependencies' is dynamic but already listed in [project]."
            )

        has_optional_dependencies = "optional-dependencies" in metadata
        if is_dynamic_optional_dependencies and has_optional_dependencies:
            raise ValueError(
                "'optional-dependencies' is dynamic but already listed in [project]."
            )

        has_dependencies = self.plugin_config.dependencies is not None
        has_optional_dependencies = self.plugin_config.optional_dependencies is not None
        if not (has_dependencies or has_optional_dependencies):
            raise ValueError(
                "No dependencies or optional-dependencies found in the plugin config."
            )

        rendered_dependencies = self.render_dependencies()
        if rendered_dependencies:
            metadata["dependencies"] = rendered_dependencies

        rendered_optional_dependencies = self.render_optional_dependencies()
        if rendered_optional_dependencies:
            metadata["optional-dependencies"] = rendered_optional_dependencies
