from rank_bm25 import BM25Okapi
from .store_base import VectorStoreBase

class BM25KeywordStore(VectorStoreBase):
    def __init__(self):
        self.corpus = []
        self.bm25 = None
        self.metadatas = []

    def add_documents(self, chunks, embeddings=None, metadatas=None):
        self.corpus.extend([chunk["text"] for chunk in chunks])
        self.metadatas.extend(metadatas or [{} for _ in chunks])
        self.bm25 = BM25Okapi([doc.split(" ") for doc in self.corpus])

    def search(self, query_text, k=5, method=None):
        scores = self.bm25.get_scores(query_text.split(" "))
        best_idx = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
        return [
            {"text": self.corpus[i], "meta": self.metadatas[i], "score": scores[i]}
            for i in best_idx
        ]
