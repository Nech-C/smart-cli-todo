from src.core import search_task


def test_search_task(monkeypatch, semantic_tracker):
    def fake_search(query, k):
        return [({"q": query}, 0.5), ({"x": "y"}, 0.4)]

    monkeypatch.setattr("src.core.search_task_vector", fake_search)
    results = search_task("foo", k=2)
    assert list(results) == [{"q": "foo"}, {"x": "y"}]
    # TODO: finish tests
