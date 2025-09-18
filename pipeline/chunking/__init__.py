from .fixed_chunker import FixedChunker
from .semantic_chunker import SemanticChunker

def chunk_text(text: str, chunk_size: int, overlap: int, method="fixed"):
    if method == "fixed":
        return FixedChunker().chunk(text, chunk_size, overlap)
    elif method == "semantic":
        return SemanticChunker().chunk(text, chunk_size, overlap)
    else:
        raise ValueError("Unknown chunking method: " + str(method))