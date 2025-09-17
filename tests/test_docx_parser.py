import os
from pipeline.ingest.docx_parser import DOCXParser

def test_docx_extraction():
    test_docx = "data/samples/sample.docx"
    assert os.path.exists(test_docx), "Test DOCX not found."
    parser = DOCXParser()
    text, metadata = parser.extract_text_and_metadata(test_docx)
    assert isinstance(text, str) and len(text) > 0
    assert metadata["filetype"] == "docx"