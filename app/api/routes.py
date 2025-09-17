from fastapi import APIRouter, File, UploadFile
from pathlib import Path
from pipeline.ingest.pdf_parser import PDFParser
from pipeline.ingest.docx_parser import DOCXParser
from pipeline.ingest.txt_parser import TXTParser
from pipeline.ingest.html_parser import HTMLParser


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
    return {"filename": file.filename, "preview": text[:500], "metadata": metadata}
