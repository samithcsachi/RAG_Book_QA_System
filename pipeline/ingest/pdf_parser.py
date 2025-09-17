import fitz  
from pathlib import Path
from .parser_base import ParserBase
from typing import Tuple, Dict 

class PDFParser(ParserBase):
    def extract_text_and_metadata(self, filepath: str) -> Tuple[str, Dict]:
        
        doc = fitz.open(filepath)
        text = ""
        pages_metadata = []
        for i, page in enumerate(doc):
            page_text = page.get_text()
            text += page_text + "\n"
            pages_metadata.append({
                "page_num": i+1,
                "length": len(page_text),
                'first_100_chars': page_text[:100], 
            })
        metadata = {
            "filetype": "pdf",
            "n_pages": doc.page_count,
            "pages": pages_metadata,
            "filename": str(Path(filepath).name)
        }
        return text, metadata
