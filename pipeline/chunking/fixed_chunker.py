from typing import List, Dict
from .splitter_base import SplitterBase

class FixedChunker(SplitterBase):
    def chunk(self, text: str, chunk_size: int, overlap: int) -> List[Dict]:
        chunks = []
        idx = 0
        while idx < len(text):
            end = min(idx + chunk_size, len(text))
            chunk_text = text[idx:end]
            chunks.append({
                "text": chunk_text,
                "start": idx,
                "end": end,
                "meta": {"source": "fixed"}
            })
            if end == len(text):
                break
            idx += chunk_size - overlap
        return chunks
