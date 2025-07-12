import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Dynamic Getters ---


def get_data_dir() -> Path:
    return Path(os.environ.get("LLM_TODO_DATA_DIR", "~/.llm-todo")).expanduser()


def get_config_name() -> str:
    return os.environ.get("LLM_TODO_CONFIG_PATH", "config.json")


def get_task_name() -> str:
    return os.environ.get("LLM_TODO_TASK_NAME", "tasks.json")


def get_config_path() -> Path:
    return get_data_dir() / get_config_name()


def get_task_path() -> Path:
    return get_data_dir() / get_task_name()


# --- Core Functions ---


def init(task_file_path: str = None) -> dict:
    """Initialize and create config and task files.

    Args:
        task_file_path (str, optional): The path to the task file. If None,
        it defaults to ~/.llm-todo/tasks.json or the env override.

    Returns:
        dict: The written config dictionary.
    """
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)

    if not task_file_path:
        task_file_path = str(get_task_path())

    config = {"task_file": task_file_path}
    config_path = get_config_path()

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    if not os.path.exists(task_file_path):
        with open(task_file_path, "w") as f:
            json.dump({"tasks": []}, f, indent=2)

    return config


def load_config() -> dict:
    """Load and return the current config."""
    with open(get_config_path(), "r") as f:
        return json.load(f)


def update_config(new_values: dict):
    """Update config values and write back to disk."""
    config = load_config()
    config.update(new_values)
    with open(get_config_path(), "w") as f:
        json.dump(config, f, indent=2)
