import tempfile
import pytest
from src.config import init

@pytest.fixture
def isolated_config_env(monkeypatch):
    """Creates a temp config dir and runs init(). Cleans up after test."""
    with tempfile.TemporaryDirectory() as temp_dir:
        monkeypatch.setenv("LLM_TODO_DATA_DIR", temp_dir)
        config = init()
        yield config
        # temp_dir is deleted automatically
