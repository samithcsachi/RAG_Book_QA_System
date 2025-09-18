import re
from typing import List, Dict
from .splitter_base import SplitterBase

HEADING_PATTERNS = [
    r"^(CHAPTER|Chapter|Section)\s+\d+",
    r"^[A-Z][A-Z ]{5,}$",
    r"^(\d+\.){1,3}\s+\w+",
]
PAGE_PATTERN = re.compile(r"\b[Pp]age\s+(\d+)\b|\f")
FIGURE_PATTERN = re.compile(r"^(Figure|Table|Image)[ .:]+\d+[ .:]+", re.IGNORECASE)

def find_headings(lines):
    headings = []
    for i, line in enumerate(lines):
        for pat in HEADING_PATTERNS:
            if re.match(pat, line.strip()):
                headings.append((i, line.strip()))
                break
    return headings

def split_by_size(text, chunk_size, overlap):
    
    subsections = []
    i = 0
    while i < len(text):
        end_i = min(i + chunk_size, len(text))
        chunk = text[i:end_i]
        if chunk.strip():
            subsections.append((i, end_i, chunk))
        if end_i == len(text):
            break
        i += chunk_size - overlap
    return subsections

class SemanticChunker(SplitterBase):
    def chunk(self, text: str, chunk_size: int, overlap: int) -> List[Dict]:
        lines = text.splitlines()
        cur_section = None
        cur_page = 1
        chunks = []

        line_pages = {}
        for i, line in enumerate(lines):
            m = PAGE_PATTERN.search(line)
            if m and m.group(1):
                cur_page = int(m.group(1))
            line_pages[i] = cur_page

        i = 0
        while i < len(lines):
            line = lines[i]
           
            if any(re.match(pat, line.strip()) for pat in HEADING_PATTERNS):
                cur_section = line.strip()
                i += 1
                continue
           
            if FIGURE_PATTERN.match(line):
                chunks.append({
                    "text": line.strip(),
                    "start": i,
                    "end": i + 1,
                    "meta": {
                        "section": cur_section or "NO_SECTION",
                        "page": line_pages.get(i, 1),
                        "type": "figure"
                    }
                })
                i += 1
                continue
          
            if PAGE_PATTERN.search(line):
                i += 1
                continue
           
            para_lines = []
            para_start = i
            while (i < len(lines) and lines[i].strip() and
                   not any(re.match(pat, lines[i].strip()) for pat in HEADING_PATTERNS) and
                   not FIGURE_PATTERN.match(lines[i]) and
                   not PAGE_PATTERN.search(lines[i])):
                para_lines.append(lines[i])
                i += 1
            para_text = "\n".join(para_lines).strip()
            
            if para_text:
                subchunks = split_by_size(para_text, chunk_size, overlap)
                for substart, subend, chunk_str in subchunks:
                    chunks.append({
                        "text": chunk_str,
                        "start": para_start,  
                        "end": i,            
                        "meta": {
                            "section": cur_section or "NO_SECTION",
                            "page": line_pages.get(para_start, 1),
                            "source": "semantic"
                        }
                    })
           
            while i < len(lines) and not lines[i].strip():
                i += 1
        return chunks
