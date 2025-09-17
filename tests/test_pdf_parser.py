import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline.ingest.pdf_parser import PDFParser
import os

def test_pdf_extraction():
    test_pdf = "data/samples/sample.pdf"
    assert os.path.exists(test_pdf), "Test PDF not found."
    parser = PDFParser()
    text, metadata = parser.extract_text_and_metadata(test_pdf)
    assert isinstance(text, str) and len(text) > 0
