from .faiss_store import VectorStoreFAISS
from .bm25_keyword_store import BM25KeywordStore
from .hybrid_retriever import HybridRetriever

def get_store(store_type, **kwargs):
    if store_type == "faiss":
        return VectorStoreFAISS(**kwargs)
    elif store_type == "bm25":
        return BM25KeywordStore()
    elif store_type == "hybrid":
        # Accepts 'dim', 'alpha'
        faiss_store = VectorStoreFAISS(kwargs["dim"])
        bm25_store = BM25KeywordStore()
        return HybridRetriever(faiss_store, bm25_store, kwargs.get("alpha", 0.5))
    else:
        raise ValueError(f"Unknown store type: {store_type}")
