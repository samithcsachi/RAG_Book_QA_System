import gradio as gr
from pathlib import Path
import os
import re

from pipeline.ingest.pdf_parser import PDFParser
from pipeline.ingest.docx_parser import DOCXParser
from pipeline.ingest.txt_parser import TXTParser
from pipeline.ingest.html_parser import HTMLParser
from pipeline.chunking.fixed_chunker import FixedChunker
from pipeline.embeddings.sentence_transformer_embed import embed_chunks
from pipeline.vector_store.faiss_store import FaissStore
from pipeline.rag.retrieval_engine import answer_question

FAISS_INDEX_PATH = "data/faiss.index"
EMBED_DIM = 384

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

def process_and_qa(file, question):
    try:
        save_dir = Path("data/raw/")
        save_dir.mkdir(parents=True, exist_ok=True)
        filename = sanitize_filename(getattr(file, "name", "uploaded_file"))
        file_path = save_dir / Path(filename).name

        content = None
        if hasattr(file, "read"):
            content = file.read()
        elif hasattr(file, "data"):
            content = file.data
        elif isinstance(file, bytes):
            content = file
        elif isinstance(file, str) and os.path.exists(file):
            content = None
            file_path = file
        else:
            return "Invalid file object format!", "Error", "Error"

        if content:
            with open(file_path, "wb") as f:
                f.write(content)

        ext = Path(filename).suffix.lower()
        if ext == ".pdf":
            parser = PDFParser()
        elif ext == ".docx":
            parser = DOCXParser()
        elif ext == ".txt":
            parser = TXTParser()
        elif ext in [".html", ".htm"]:
            parser = HTMLParser()
        else:
            return "Unsupported filetype.", "", ""

        
        try:
            text, metadata = parser.extract_text_and_metadata(str(file_path))
            chunks = FixedChunker().chunk(text, chunk_size=512, overlap=64)
            #print(f"Chunks parsed: {len(chunks)}")
            embeddings = embed_chunks(chunks, model_name="all-MiniLM-L6-v2")
            #print(f"Embeddings computed: {len(embeddings)}")
            metadatas = [{} for _ in chunks]
            store = FaissStore(dim=EMBED_DIM, index_path=FAISS_INDEX_PATH)
            if os.path.exists(FAISS_INDEX_PATH):
                store.load()
            store.add_documents(chunks, embeddings, metadatas)
            store.save()
            #print("Index updated.")
        except Exception as e:
            return f"Failed to extract: {repr(e)}", "", ""

        qa_result = answer_question(
            question=question,
            embed_model="all-MiniLM-L6-v2",
            store_type="faiss",
            store_kwargs={"dim": EMBED_DIM, "index_path": FAISS_INDEX_PATH},
            llm_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            top_k=5,
        )
        answer = qa_result["answer"]
        matched_chunks = qa_result.get("chunks", [])
        #print("QA chunks:", matched_chunks)
        context = "\n\n---\n\n".join([c["text"] for c in matched_chunks]) if matched_chunks else "No supporting context found."
        return f"Preview (first 500 chars):\n{text[:500]}", answer, context

    except Exception as e:
        # print("GRADIO ERROR:", str(e))
        return f"Error: {e}", "Error", "Error"

iface = gr.Interface(
    fn=process_and_qa,
    inputs=[
        gr.File(label="Upload PDF, DOCX, TXT, or HTML"),
        gr.Textbox(label="Question"),
    ],
    outputs=[
        gr.Textbox(label="Extracted/Text Preview", lines=10, show_copy_button=True),
        gr.Textbox(label="Answer", lines=6, show_copy_button=True),
        gr.Textbox(label="Matched Context", lines=12, show_copy_button=True)
    ],
    title="Book/Document QA",
    description="Upload your document, ask a question, and see the answer with cited context!"
)

if __name__ == "__main__":
    iface.launch()
