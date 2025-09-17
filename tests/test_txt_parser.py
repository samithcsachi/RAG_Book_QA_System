import os
from pipeline.ingest.txt_parser import TXTParser

def test_txt_extraction():
    test_txt = "data/samples/sample.txt"
    assert os.path.exists(test_txt), "Test TXT not found."
    parser = TXTParser()
    text, metadata = parser.extract_text_and_metadata(test_txt)
    assert isinstance(text, str) and len(text) > 0
    assert metadata["filetype"] == "txt"