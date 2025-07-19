from core import _index_tasks, search_task


def test_index_tasks(monkeypatch, semantic_tracker):
    tasks = [
        {"id": "1", "indexed": False},
        {"id": "2", "indexed": True},
    ]
    monkeypatch.setattr('core.load_tasks_from_storage', lambda: tasks)
    _index_tasks()
    assert semantic_tracker['add'] == [tasks[0]]


def test_search_task(monkeypatch, semantic_tracker):
    monkeypatch.setattr('core._index_tasks', lambda: semantic_tracker["add"].append("called"))

    def fake_search(query, k):
        return [({"q": query}, 0.5), ({"x": "y"}, 0.4)]

    monkeypatch.setattr('core.search_task_vector', fake_search)
    results = search_task('foo', k=2)
    assert list(results) == [{"q": "foo"}, {"x": "y"}]
    assert semantic_tracker['add'] == ['called']
