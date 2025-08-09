# smart-cli-todo
A command line to-do list tool powered by an LLM backend. Tasks are stored locally in JSON and indexed in a Chroma vector store for semantic search.

## Installation
1. **Prerequisites** – Python 3.13 or newer.
2. Clone this repository and install in editable mode:
```bash
pip install -e .
```
3. Initialise the configuration and data files (created under `~/.llm-todo` by default):
```bash
llm-todo init
```
   Use the environment variable `LLM_TODO_DATA_DIR` if you want the data elsewhere.
4. Install ollama and download qwen
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:0.5b
```
## Usage
### Add
```bash
llm-todo add pay rent /d2000 dollars /2030-05-01 /repeat
```
Adds a recurring task due on 1 May 2030 with a description of "2000 dollars".

### List
```bash
llm-todo list        # pending tasks
llm-todo list done   # completed tasks
llm-todo list all    # everything
```

### Finish
Mark one or more tasks as completed. The command prompts you to choose:
```bash
llm-todo finish
```

### Remove
Remove tasks interactively:
```bash
llm-todo remove      # default shows ongoing tasks
```
Use `llm-todo remove done` or `llm-todo remove all` to pick from completed or all tasks.

### Update
Update a task by number with new values:
```bash
llm-todo update 2 new name /d updated description /2030-06-01
```

### Undo
Revert the last add, remove, update or finish action:
```bash
llm-todo undo
```

### Search
Semantic search over your tasks (pending changes to the vector index are automatically committed):
```bash
llm-todo search "pay rent"
```

### Init
Recreate configuration and data files:
```bash
llm-todo init
```

## Notes
* Vector store operations are **lazy**. When you add or remove tasks the changes are queued. Running a search (or calling `commit_vector_tasks` manually) applies all pending updates.
* All data lives in `~/.llm-todo` unless `LLM_TODO_DATA_DIR` is set.

This project is licensed under the Apache 2.0 license.
