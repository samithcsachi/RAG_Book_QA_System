from .faiss_store import VectorStoreFAISS
from .bm25_keyword_store import BM25KeywordStore
from .store_base import VectorStoreBase

class HybridRetriever(VectorStoreBase):
    def __init__(self, faiss_store, bm25_store, alpha=0.5):
        self.faiss_store = faiss_store
        self.bm25_store = bm25_store
        self.alpha = alpha

    def add_documents(self, chunks, embeddings, metadatas):
        self.faiss_store.add_documents(chunks, embeddings, metadatas)
        self.bm25_store.add_documents(chunks, None, metadatas)

    def search(self, query_embed, query_text, k=5, method=None):
        faiss_hits = self.faiss_store.search(query_embed, k)
        bm25_hits = self.bm25_store.search(query_text, k)

        # Simple hybrid: combine and sort by average rank/score (tune as desired)
        faiss_ids = {hit["text"]: i for i, hit in enumerate(faiss_hits)}
        bm25_ids = {hit["text"]: i for i, hit in enumerate(bm25_hits)}
        all_texts = set(faiss_ids) | set(bm25_ids)

        hybrid = []
        for text in all_texts:
            f_rank = faiss_ids.get(text, k)
            b_rank = bm25_ids.get(text, k)
            joint_score = self.alpha * (k - f_rank) + (1 - self.alpha) * (k - b_rank)
            # Prefer faiss meta but fallback to bm25
            meta = faiss_hits[faiss_ids[text]]["meta"] if text in faiss_ids else bm25_hits[bm25_ids[text]]["meta"]
            hybrid.append({"text": text, "meta": meta, "score": joint_score})
        return sorted(hybrid, key=lambda x: -x["score"])[:k]
