from . import sentence_transformer_embed

EMBEDDING_BACKENDS = {
    "sentence_transformers": sentence_transformer_embed
}

def embed_chunks(chunks, backend: str, model_name: str, version: str = None):
    mod = EMBEDDING_BACKENDS.get(backend)
    if not mod:
        raise ValueError(f"Unknown backend: {backend}")
    texts = [c["text"] if isinstance(c, dict) else c for c in chunks]
    metas = [c.get("meta", {}) if isinstance(c, dict) else {} for c in chunks]
    embeddings = mod.embed(texts, model_name)
    version = version or f"{backend}:{model_name}"
    return [
        {"embedding": emb, "meta": meta, "version": version}
        for emb, meta in zip(embeddings, metas)
    ]
