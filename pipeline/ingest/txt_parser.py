from pathlib import Path
from .parser_base import ParserBase
from typing import Tuple, Dict 

class TXTParser(ParserBase):
    def extract_text_and_metadata(self, filepath: str) -> Tuple[str, Dict]:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        metadata = {
            "filetype": "txt",
            "filename": str(Path(filepath).name),
            "length": len(text)
        }
        return text, metadata
    
