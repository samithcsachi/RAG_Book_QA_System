from sentence_transformers import SentenceTransformer

def embed(texts, model_name="all-MiniLM-L6-v2"):
   
    model = SentenceTransformer(model_name)
    return model.encode(texts, show_progress_bar=False, convert_to_numpy=True).tolist()
