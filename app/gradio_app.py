import gradio as gr
from pipeline.ingest.pdf_parser import PDFParser
from pipeline.ingest.docx_parser import DOCXParser
from pipeline.ingest.txt_parser import TXTParser
from pipeline.ingest.html_parser import HTMLParser
from pathlib import Path
import time

def extract_and_save(file):
    save_dir = Path("data/raw/")
    save_dir.mkdir(parents=True, exist_ok=True)
    filename = getattr(file, "name", None)
    if not filename:
        filename = f"upload_{int(time.time())}.bin"
    file_path = save_dir / Path(filename).name

    if file_path.exists():
        file_path.unlink()

   
    if isinstance(file, bytes):
        content = file
    elif hasattr(file, "read"):
        file.seek(0)
        content = file.read()
    elif isinstance(file, str):
        content = file.encode("latin1")
    else:
        return "Unknown file object! Please upload a PDF, DOCX, TXT, or HTML file."

    with open(file_path, "wb") as f:
        f.write(content)

    ext = Path(filename).suffix.lower()

    parser = None
    if ext == ".pdf":
        parser = PDFParser()
    elif ext == ".docx":
        parser = DOCXParser()
    elif ext == ".txt":
        parser = TXTParser()
    elif ext == ".html" or ext == ".htm":
        parser = HTMLParser()
    else:
        
        try:
         
            text_sample = content.decode("utf-8", errors="ignore")
            if "<html" in text_sample.lower():
                parser = HTMLParser()
                file_path = file_path.with_suffix(".html")
            else:
                content.decode("utf-8")  
                parser = TXTParser()
                file_path = file_path.with_suffix(".txt")
            with open(file_path, "wb") as f:
                f.write(content)
        except Exception:
            return "Unsupported file type!"

    try:
        text, metadata = parser.extract_text_and_metadata(str(file_path))
        output = f"First 500 characters:\n\n{text[:500]}"
    except Exception as e:
        output = f"Failed to extract {ext[1:] if ext else 'file'}: {repr(e)}"
    return output

demo = gr.Interface(
    fn=extract_and_save,
    inputs=gr.File(type="binary", label="Upload PDF, DOCX, TXT, or HTML"),
    outputs="text",
    title="Document Text Extractor"
)

if __name__ == "__main__":
    demo.launch()
