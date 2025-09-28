from sentence_transformers import SentenceTransformer


def embed(texts, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    return model.encode(texts, show_progress_bar=False,
                        convert_to_numpy=True).tolist()


def embed_chunks(chunks, model_name="all-MiniLM-L6-v2"):

    texts = [chunk['text'] for chunk in chunks]
    return embed(texts, model_name=model_name)
