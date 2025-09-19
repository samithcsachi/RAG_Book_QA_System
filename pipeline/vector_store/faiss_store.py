import faiss
import numpy as np
import pickle
from .store_base import VectorStoreBase

class VectorStoreFAISS(VectorStoreBase):
    def __init__(self, dim, index_path=None, metadata_path=None):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.embeddings = []
        self.metadatas = []
        self.texts = []
        self.index_path = index_path or "faiss.index"
        self.metadata_path = metadata_path or "faiss.meta.pkl"

    def add_documents(self, chunks, embeddings, metadatas):
        arr = np.array(embeddings).astype('float32')
        self.index.add(arr)
        self.embeddings.extend(embeddings)
        self.texts.extend([chunk["text"] for chunk in chunks])
        self.metadatas.extend(metadatas)
        self.save()

    def search(self, query_embed, k=5, method=None):
        query = np.array(query_embed).reshape(1, -1).astype('float32')
        D, I = self.index.search(query, k)
        results = []
        for idx in I[0]:
            if idx >= 0 and idx < len(self.texts):
                results.append({
                    "text": self.texts[idx],
                    "embedding": self.embeddings[idx],
                    "meta": self.metadatas[idx]
                })
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump({
                "texts": self.texts,
                "embeddings": self.embeddings,
                "metadatas": self.metadatas
            }, f)

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, "rb") as f:
            data = pickle.load(f)
            self.texts = data["texts"]
            self.embeddings = data["embeddings"]
            self.metadatas = data["metadatas"]
