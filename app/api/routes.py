from fastapi import APIRouter, File, UploadFile
from pathlib import Path
from pipeline.ingest.pdf_parser import PDFParser
from pipeline.ingest.docx_parser import DOCXParser
from pipeline.ingest.txt_parser import TXTParser
from pipeline.ingest.html_parser import HTMLParser
from fastapi import Request
from pipeline.rag.retrieval_engine import answer_question
import logging

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    save_dir = Path("data/raw/")
    save_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename).suffix.lower()
    file_path = save_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    if ext == ".pdf":
        parser = PDFParser()
    elif ext == ".docx":
        parser = DOCXParser()
    elif ext == ".txt":
        parser = TXTParser()
    elif ext in [".html", ".htm"]:
        parser = HTMLParser()
    else:
        return {"error": "Unsupported file type!"}

    text, metadata = parser.extract_text_and_metadata(str(file_path))
    return {"filename": file.filename,
            "preview": text[:500],
            "metadata": metadata}


@router.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")
    if not question:
        return {"error": "No question provided."}

    answer_pack = answer_question(
        question=question,
        embed_model="all-MiniLM-L6-v2",
        store_type="faiss",
        store_kwargs={"dim": 384},
        llm_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        top_k=3,
    )
    logging.info(f"Question answered: '{question}'")
    return {
        "answer": answer_pack["answer"],
        "chunks": answer_pack["chunks"],
        "context": answer_pack["context"]
    }


@router.post("/feedback")
async def feedback(request: Request):
    data = await request.json()
    with open("feedback.csv", "a") as f:
        f.write(
            f"{
                data.get(
                    'question', '')},{
                data.get(
                    'answer', '')},{
                        data.get(
                            'rating', '')}\n")
    logging.info(f"Feedback received for: '{data.get('question', '')}'")
    return {"success": True}
