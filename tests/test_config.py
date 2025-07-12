from pathlib import Path
from src.config import get_config_path, get_task_path, load_config, update_config

def test_init(isolated_config_env):
    config_path = get_config_path()
    task_path = get_task_path()
    config = isolated_config_env

    assert config_path.exists()
    assert task_path == Path(config["task_file"])
    assert task_path.exists()

def test_load_config(isolated_config_env):
    loaded_config = load_config()
    assert loaded_config == isolated_config_env

def test_update_config(isolated_config_env):
    new_values = { "test": "test", "task_file": "new_path.json" }
    expected = isolated_config_env.copy()
    expected.update(new_values)

    update_config(new_values)
    new_config = load_config()

    assert new_config == expected
