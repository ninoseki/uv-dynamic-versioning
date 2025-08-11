import pytest

from uv_dynamic_versioning import schemas


def test_bump_config():
    config = schemas.BumpConfig.from_dict({"enable": True, "index": 2})
    assert config.enable is True
    assert config.index == 2


def test_bump_config_invalid_index():
    with pytest.raises(ValueError):
        schemas.BumpConfig.from_dict({"enable": True, "index": "not-an-int"})


def test_uv_dynamic_versioning_from_dict_valid():
    data = {
        "vcs": "git",
        "metadata": True,
        "bump": {"enable": True, "index": 1},
    }
    config = schemas.UvDynamicVersioning.from_dict(data)
    assert config.vcs.name == "Git"
    assert config.metadata is True
    assert isinstance(config.bump, schemas.BumpConfig)


def test_uv_dynamic_versioning_invalid_vcs():
    with pytest.raises(ValueError):
        schemas.UvDynamicVersioning.from_dict({"vcs": "invalid-vcs"})


def test_tool_from_dict_valid():
    data = {
        "uv_dynamic_versioning": {
            "vcs": "git",
            "metadata": False,
        }
    }
    tool = schemas.Tool.from_dict(data)
    assert isinstance(tool.uv_dynamic_versioning, schemas.UvDynamicVersioning)
    assert tool.uv_dynamic_versioning.vcs.name == "Git"


def test_tool_from_dict_invalid():
    with pytest.raises(ValueError):
        schemas.Tool.from_dict({"uv_dynamic_versioning": "not-a-dict"})


def test_project_from_dict_valid():
    data = {"tool": {"uv_dynamic_versioning": {"vcs": "git"}}}
    project = schemas.Project.from_dict(data)
    assert isinstance(project.tool, schemas.Tool)
    assert isinstance(project.tool.uv_dynamic_versioning, schemas.UvDynamicVersioning)


def test_project_from_dict_missing_tool():
    with pytest.raises(ValueError):
        schemas.Project.from_dict({})


def test_metadata_hook_config_valid():
    data = {"dependencies": ["a", "b"], "optional_dependencies": {"extra": ["c", "d"]}}
    config = schemas.MetadataHookConfig.from_dict(data)
    assert config.dependencies == ["a", "b"]
    assert config.optional_dependencies == {"extra": ["c", "d"]}


def test_metadata_hook_config_invalid_dependencies():
    with pytest.raises(ValueError):
        schemas.MetadataHookConfig.from_dict({"dependencies": "not-a-list"})


def test_metadata_hook_config_invalid_optional_dependencies():
    with pytest.raises(ValueError):
        schemas.MetadataHookConfig.from_dict({"optional_dependencies": "not-a-dict"})
