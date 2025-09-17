import os
from pipeline.ingest.html_parser import HTMLParser

def test_html_extraction():
    test_html = "data/samples/sample.html"
    assert os.path.exists(test_html), "Test HTML not found."
    parser = HTMLParser()
    text, metadata = parser.extract_text_and_metadata(test_html)
    assert isinstance(text, str) and len(text) > 0
    assert metadata["filetype"] == "html"