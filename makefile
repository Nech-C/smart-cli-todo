clear-config:
	rm -rf ~/.llm-todo

clear-all:
	clearn_config

test-all:
	PYTHONPATH=. uv run pytest tests/
