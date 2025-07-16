from typing import Union, List
from functools import lru_cache

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import get_embedder_repo, get_chroma_dir


@lru_cache(maxsize=1)
def _get_embedder():
    return HuggingFaceEmbeddings(model_name=get_embedder_repo())


@lru_cache(maxsize=1)
def _get_vector_store():
    return Chroma("todo_list", _get_embedder(), get_chroma_dir())


def add_task_vector(task: dict):
    text = task.get("text")
    metadata = task.get("metadata")
    id_ = task.get("id")
    if id_ is None:
        print("No id provided.")
        return
    _get_vector_store().add_texts(texts=[text], metadatas=[metadata], ids=[id_])


def search_task_vector(query: str, k: int) -> list:
    return _get_vector_store().similarity_search_with_score(query, k=k)


def remove_task_vector(ids: Union[str, List[str]]):
    if isinstance(ids, str):
        ids = [ids]
    _get_vector_store().delete(ids)
