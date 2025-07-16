import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


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


def get_history_path() -> Path:
    # for undo
    return get_data_dir() / "last_action.json"


def init(task_file_path: str = None) -> dict:
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)

    if not task_file_path:
        task_file_path = str(get_task_path())

    config = {
        "task_file": task_file_path,
        "chroma_dir": str(get_data_dir() / "chroma_db"),
        "hf_embedder_repo": "all-MiniLM-L6-v2",
    }
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    # ensure the two JSON stores exist
    if not os.path.exists(task_file_path):
        with open(task_file_path, "w") as f:
            json.dump({"tasks": []}, f, indent=2)
    hist = get_history_path()
    if not hist.exists():
        hist.write_text("")  # start empty

    return config


def load_config() -> dict:
    try:
        with open(get_config_path(), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        init()
        return load_config()


def update_config(new_values: dict):
    config = load_config()
    config.update(new_values)
    with open(get_config_path(), "w") as f:
        json.dump(config, f, indent=2)


def get_embedder_repo() -> str:
    config = load_config()
    return config["hf_embedder_repo"]


def get_chroma_dir() -> Path:
    config = load_config()
    return config["chroma_dir"]
