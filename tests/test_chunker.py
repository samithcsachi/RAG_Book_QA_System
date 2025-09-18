import sys
import os

from pipeline.chunking import chunk_text


def test_fixed_chunker():
    text = "abcdefghij" * 100
    chunks = chunk_text(text, chunk_size=50, overlap=10, method="fixed")
    assert all(len(c["text"]) <= 50 for c in chunks)
    assert chunks[1]["start"] == 40  # checks overlap
    assert "meta" in chunks[0]

def test_semantic_chunker():
    text = "Intro para.\n\nSecond para is here.\n\nThird para."
    chunks = chunk_text(text, chunk_size=25, overlap=0, method="semantic")
    assert all(len(c["text"]) <= 25 for c in chunks)
    assert all("meta" in c for c in chunks)



def test_semantic_chunker_with_sections():
    text = (
        "CHAPTER 1\n"
        "This is the start of chapter one. " * 8 + "\n\n"
        "Section 1.1\n"
        "Subsection text here. " * 10 + "\n\n"
        "CHAPTER 2\n"
        "Now we are in chapter two. " * 6
    )
    chunk_size = 100
    overlap = 20
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap, method="semantic")
    prev_section = None
    for chunk in chunks:
        # Each chunk should have a section label
        assert "section" in chunk["meta"]
        # Each chunk's section label should actually exist in the input
        assert chunk["meta"]["section"] in text
        # Print output for manual verification (optional)
        print(f'Section: {chunk["meta"]["section"]} | Text: {chunk["text"][:40]}...')
        prev_section = chunk["meta"]["section"]

    print(f"Generated {len(chunks)} chunks.")


if __name__ == "__main__":
    test_semantic_chunker_with_sections()
