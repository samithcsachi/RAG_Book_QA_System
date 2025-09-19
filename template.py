import os 
from pathlib import Path
import logging 


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logfile.txt"),
        logging.StreamHandler()
    ]
)


project_name = 'RAG_Book_QA_System'

list_of_files = [
    # CI/CD
    ".github/workflows/ci.yml",

    # App Layer—APIs, UI, dashboard
    "app/__init__.py"
    "app/main.py",
    "app/api/__init__.py",
    "app/api/routes.py",
    "app/api/schemas.py",
    "app/api/session.py",
    "app/gradio_app.py",
    "app/dashboard.py",
    "app/logger.py",

    # Ingestion & Preprocessing
    "pipeline/__init__.py",
    "pipeline/ingest/__init__.py",
    "pipeline/ingest/parser_base.py",
    "pipeline/ingest/pdf_parser.py",
    "pipeline/ingest/docx_parser.py",
    "pipeline/ingest/txt_parser.py",
    "pipeline/ingest/html_parser.py",
    "pipeline/preprocess/__init__.py",
    "pipeline/preprocess/clean_text.py",
    "pipeline/preprocess/metadata.py",

    # Chunking & Evaluation Data
    "pipeline/chunking/__init__.py",
    "pipeline/chunking/splitter_base.py",
    "pipeline/chunking/fixed_chunker.py",
    "pipeline/chunking/semantic_chunker.py",
    "pipeline/chunking/chunk_benchmark.py",
    "pipeline/eval_data/__init__.py",
    "pipeline/eval_data/qa_generator.py",

    # Embeddings
    "pipeline/embeddings/__init__.py",
    "pipeline/embeddings/embedder_base.py",
    "pipeline/embeddings/sentence_transformer_embed.py",
       

    # Vector Store & Hybrid Retrieval
    "pipeline/vector_store/__init__.py",
    "pipeline/vector_store/store_base.py",
    "pipeline/vector_store/faiss_store.py",
    "pipeline/vector_store/bm25_keyword_store.py",
    "pipeline/vector_store/store_registry.py",
    "pipeline/vector_store/hybrid_retriever.py",

    # Core RAG & Metrics
    "pipeline/rag/__init__.py",
    "pipeline/rag/retrieval_engine.py",
    "pipeline/rag/prompt_templates.py",
   
    
    # Monitoring/Feedback
    "pipeline/monitoring/__init__.py",
    "pipeline/monitoring/drift_detection.py",
    "pipeline/monitoring/feedback.py",

    # LLM registry/wrappers
    "llm/__init__.py",
    "llm/llm_base.py",
    "llm/model_registry.py",
   

    # Automated Tests
    "tests/__init__.py",
    "tests/test_pdf_parser.py",
    "tests/test_docx_parser.py", 
    "tests/test_txt_parser.py",
    "tests/test_html_parser.py",
    "tests/test_chunker.py",
    "tests/test_embedder.py",
    "tests/test_vector_store.py",
    "tests/test_rag_engine.py",
    "tests/test_llm.py",

    # Data, config, infra
    "data/samples/.gitkeep",
    "docker/Dockerfile",
    "docker/docker-compose.yml",
    "Makefile",
    "requirements.txt",
    "README.md",
    ".gitignore",
    ".env.example",
    "config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",

    # Documentation for deployment & privacy
    "docs/deploy_hf_spaces.md",
    "docs/deploy_aws_ec2.md",
    "docs/deploy_streamlit.md",
    "docs/security_privacy.md",

    # Research/experimentation notebooks
    "research/01_data_profiling.ipynb",
    "research/02_parser_pipeline_experiments.ipynb",
    "research/03_chunking_strategy_tests.ipynb",
    "research/04_embedding_comparison.ipynb",
    "research/05_retrieval_eval_and_metrics.ipynb",
    "research/06_prompt_and_llm_experiments.ipynb"
]


for file_path in list_of_files:
    file_path = Path(file_path)
    file_dir, filename = os.path.split(file_path)
   
    if file_dir !="":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Created directory: {file_dir} for the file: {filename}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, 'w') as f:
            pass
        logging.info(f"Created empty file: {file_path}")

    else:
        logging.info(f"File already exists: {file_path} and is not empty.")
        