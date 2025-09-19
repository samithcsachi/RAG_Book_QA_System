from pipeline.rag.retrieval_engine import answer_question
from pipeline.rag.prompt_templates import DEFAULT_PROMPT_TEMPLATE

def test_rag_pipeline_e2e():
    
    response = answer_question(
        question="What is artificial intelligence?",
        embed_model="all-MiniLM-L6-v2",
        store_type="faiss",
        store_kwargs={"dim": 384},
        llm_name="mistralai/Mistral-7B-Instruct-v0.2",
        prompt_template=DEFAULT_PROMPT_TEMPLATE,
        top_k=3,
    )
    print("RAG Output:", response)
    assert "answer" in response
    assert "context" in response
    assert "chunks" in response
    assert isinstance(response["answer"], str)
