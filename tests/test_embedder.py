from pipeline.embeddings import embed_chunks  

def test_sentence_transformers_shape():
    chunks = [{"text": "Test one."}, {"text": "Another test."}]
    out = embed_chunks(chunks, backend="sentence_transformers", model_name="all-MiniLM-L6-v2")
    assert len(out) == 2
    assert "embedding" in out[0]
    dims = {len(row['embedding']) for row in out}
    assert len(dims) == 1  # All vectors same dimension

def test_embedder_metadata():
    chunks = [{"text": "foo", "meta": {"page": 1}}]
    out = embed_chunks(chunks, backend="sentence_transformers", model_name="all-MiniLM-L6-v2")
    assert "meta" in out[0]
    assert out[0]["meta"]["page"] == 1
