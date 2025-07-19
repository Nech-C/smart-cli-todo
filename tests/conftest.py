# conftest.py
import sys
import tempfile
import types
import pytest

# Provide stub replacements for optional dependencies so tests can run
dotenv_stub = types.ModuleType("dotenv")
dotenv_stub.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", dotenv_stub)

semantic_calls = {"add": [], "search": [], "remove": []}
semantic_stub = types.ModuleType("semantic")
semantic_stub.add_task_vector = lambda task: semantic_calls["add"].append(task)
semantic_stub.search_task_vector = lambda query, k=5: semantic_calls["search"].append((query, k)) or []
semantic_stub.remove_task_vector = lambda ids: semantic_calls["remove"].append(ids)
sys.modules.setdefault("semantic", semantic_stub)

from config import init


@pytest.fixture
def isolated_config_env(monkeypatch):
    """Creates a temp config dir and runs init(). Cleans up after test."""
    with tempfile.TemporaryDirectory() as temp_dir:
        monkeypatch.setenv("LLM_TODO_DATA_DIR", temp_dir)
        config = init()
        yield config
        # temp_dir is deleted automatically


@pytest.fixture
def semantic_tracker():
    """Provide access to stubbed semantic call logs."""
    for calls in semantic_calls.values():
        calls.clear()
    yield semantic_calls
