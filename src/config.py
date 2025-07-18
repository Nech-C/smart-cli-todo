import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def init(force: bool = False) -> dict:
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)

    config_path = get_config_path()
    config_exists = config_path.exists()

    if config_exists and not force:
        config = load_config()
    else:
        config = {
            "task_file": str(get_data_dir() / "tasks.json"),
            "chroma_dir": str(get_data_dir() / "chroma_db"),
            "history_file": str(get_data_dir() / "last_action.json"),
            "hf_embedder_repo": "all-MiniLM-L6-v2",
        }
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

    task_path = Path(config["task_file"])
    if force or not task_path.exists():
        with open(task_path, "w") as f:
            json.dump({"tasks": []}, f, indent=2)

    history_path = get_history_path()
    if force or not history_path.exists():
        history_path.write_text("")

    return config


def load_config() -> dict:
    with open(get_config_path(), "r") as f:
        return json.load(f)


def update_config(new_values: dict):
    config = load_config()
    config.update(new_values)
    with open(get_config_path(), "w") as f:
        json.dump(config, f, indent=2)


def get_task_path() -> Path:
    return Path(load_config()["task_file"])


def get_embedder_repo() -> str:
    return load_config()["hf_embedder_repo"]


def get_chroma_dir() -> Path:
    return Path(load_config()["chroma_dir"])


def get_data_dir() -> Path:
    return Path(os.environ.get("LLM_TODO_DATA_DIR", "~/.llm-todo")).expanduser()


def get_config_path() -> Path:
    return Path(get_data_dir() / "config.json")


def get_history_path() -> Path:
    return Path(load_config()["history_file"])
