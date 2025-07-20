# semantic.py
from typing import Union, List
from functools import lru_cache
import json

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import get_embedder_repo, get_chroma_dir, get_vector_store_queue_path


@lru_cache(maxsize=1)
def _get_embedder():
    return HuggingFaceEmbeddings(model_name=get_embedder_repo())


@lru_cache(maxsize=1)
def _get_vector_store():
    return Chroma("todo_list", _get_embedder(), str(get_chroma_dir()))


def eager_add_task_vector(task: dict):
    text = task.get("text")
    metadata = task.get("metadata")
    id_ = task.get("id")
    if id_ is None:
        print("No id provided.")
        return
    _get_vector_store().add_texts(texts=[text], metadatas=[metadata], ids=[id_])


def eager_remove_task_vector(ids: Union[str, List[str]]):
    if isinstance(ids, str):
        ids = [ids]
    _get_vector_store().delete(ids)


def lazy_vector_action(task: dict, action_type: str):
    """Add a vector store action to a queue for future execution

    Args:
        task (dict): The task to perform action on
        action_type (str): the type of action: "update", "add", and "remove"
    """
    with get_vector_store_queue_path().open() as f:
        tasks_in_queue = json.load(f)
    if action_type == "remove":
        task = {"id": task}
    task["pending_action"] = action_type
    tasks_in_queue.append(task)
    with get_vector_store_queue_path().open("w") as f:
        json.dump(tasks_in_queue, f)


def commit_vector_tasks():
    with get_vector_store_queue_path().open() as f:
        tasks_in_queue = json.load(f)
    uncommited_task = []

    # TODO: Perform only the last action per task
    for task in tasks_in_queue:
        task_type = task["pending_action"]
        try:
            if task_type == "add":
                eager_add_task_vector(task)
            elif task_type == "remove":
                eager_remove_task_vector(task["id"])
            else:
                print(f"Unknown task type {task_type}. {task['name']} is not commited.")
        except Exception as e:
            print(f"Encountered as error: {e}. Some task is not commited.")
    print(f"There are {len(uncommited_task)} uncommited tasks.")
    with get_vector_store_queue_path().open("w") as f:
        json.dump(uncommited_task, f)


def search_task_vector(query: str, k: int) -> list:
    commit_vector_tasks()
    return _get_vector_store().similarity_search_with_score(query, k=k)
