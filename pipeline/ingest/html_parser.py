from bs4 import BeautifulSoup
from pathlib import Path
from .parser_base import ParserBase
from typing import Tuple, Dict 

class HTMLParser(ParserBase):
    def extract_text_and_metadata(self, filepath: str) -> Tuple[str, Dict]:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        # Extract all visible text (ignore script, style)
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        metadata = {
            "filetype": "html",
            "filename": str(Path(filepath).name),
            "length": len(text)
        }
        return text, metadata