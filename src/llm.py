# src/llm.py

from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama

from src.config import get_ollama_model_id
from src.tools import (
    add_task_tool,
    search_task_tool,
    remove_task_tool,
    update_task_tool,
    finish_task_tool,
    list_tasks_tool,
)

TOOLS = [
    add_task_tool,
    search_task_tool,
    remove_task_tool,
    update_task_tool,
    finish_task_tool,
    list_tasks_tool,
]

SYS_PROMPT = (
    "You are an AI assisant that helps the user the manage a todo cli"
    "app. You are allowed to use tools to perform tasks on beheave of"
    " the user. Make sure only use tools when necessary."
)


_model = None
_agent = None


def _get_ollama_model():
    global _model
    if _model is None:
        _model = ChatOllama(model=get_ollama_model_id())
    return _model


def _get_langgraph_agent():
    global _agent
    if _agent is None:
        _agent = create_react_agent(
            model=_get_ollama_model(), tools=TOOLS, prompt=SYS_PROMPT
        )
    return _agent


def run(query):
    agent = _get_langgraph_agent()
    msg = agent.invoke({"messages": [("user", query)]})
    return msg
