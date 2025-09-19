class VectorStoreBase:
    def add_documents(self, chunks, embeddings, metadatas):
        raise NotImplementedError

    def search(self, query_embed=None, query_text=None, k=5, method=None):
        raise NotImplementedError
