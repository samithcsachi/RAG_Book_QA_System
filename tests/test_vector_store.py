import numpy as np
from pipeline.vector_store import get_store

def test_faiss_add_search():
    dim = 4
    # Fake data: 3 chunks, simple embeddings
    chunks = [
        {"text": "apple banana orange", "meta": {"id": 1}},
        {"text": "the cat sat on the mat", "meta": {"id": 2}},
        {"text": "openai builds ai models", "meta": {"id": 3}},
    ]
    embeddings = [
        np.array([1, 0, 0, 0]),
        np.array([0, 1, 0, 0]),
        np.array([0, 0, 1, 0]),
    ]
    store = get_store("faiss", dim=dim)
    store.add_documents(chunks, embeddings, [c["meta"] for c in chunks])
    # Query near 2nd vector
    query = [0, 0.9, 0, 0]
    results = store.search(query, k=2)
    assert len(results) == 2
    assert results[0]["meta"]["id"] == 2

def test_bm25_add_search():
    chunks = [
        {"text": "dog barks loud", "meta": {"id": 1}},
        {"text": "quiet cat with tail", "meta": {"id": 2}},
        {"text": "the quick brown fox", "meta": {"id": 3}},
    ]
    store = get_store("bm25")
    store.add_documents(chunks, None, [c["meta"] for c in chunks])
    results = store.search("cat", k=2)
    assert len(results) == 2
    assert results[0]["meta"]["id"] == 2

def test_hybrid_add_search():
    dim = 4
    chunks = [
        {"text": "gpt transformer deep learning", "meta": {"id": 1}},
        {"text": "statistical regression analysis", "meta": {"id": 2}},
        {"text": "cooking with apples and cinnamon", "meta": {"id": 3}},
    ]
    embeddings = [
        np.array([0.9, 0, 0, 0]),
        np.array([0, 0.9, 0, 0]),
        np.array([0, 0, 0.9, 0]),
    ]
    store = get_store("hybrid", dim=dim, alpha=0.5)
    store.add_documents(chunks, embeddings, [c["meta"] for c in chunks])
    results = store.search([0.85, 0.1, 0, 0], "gpt", k=2)
    ids = {r["meta"]["id"] for r in results}
    assert 1 in ids
