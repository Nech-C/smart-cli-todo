clear-config:
	rm -rf ~/.llm-todo

clear-all:
	clearn_config

test-all:
	PYTHONPATH=./src uv run pytest tests/
