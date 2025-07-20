clear-config:
	rm -rf ~/.llm-todo

clear-all:
	clearn_config

test-dummy-tasks: clear-config
	uv run main.py init
	uv run main.py add pay power bills
	uv run main.py add water plants
	uv run main.py add apply for jobs
	uv run main.py search bill
test-config:
	uv run pytest -k "config"

test-all:
	PYTHONPATH=. uv run pytest --cov=src --cov-report=term --cov-report=html tests/
