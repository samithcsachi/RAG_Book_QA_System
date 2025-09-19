from pipeline.embeddings import embed_chunks
from pipeline.vector_store import get_store
from llm import get_llm
from pipeline.rag.prompt_templates import DEFAULT_PROMPT_TEMPLATE

def answer_question(
    question: str,
    embed_model: str = "all-MiniLM-L6-v2",
    store_type: str = "faiss",
    store_kwargs: dict = None,
    llm_name: str = "mistralai/Mistral-7B-Instruct-v0.2",
    prompt_template: str = None,
    top_k: int = 5,
    rerank_fn=None,
):
    # 1. Embed query
    q_chunk = {"text": question}
    q_embed = embed_chunks([q_chunk], backend="sentence_transformers", model_name=embed_model)[0]["embedding"]

    # 2. Retrieve top-k
    if store_kwargs is None:
        store_kwargs = {"dim": 384}
    vector_store = get_store(store_type, **store_kwargs)
    if store_type == "hybrid":
        results = vector_store.search(q_embed, question, k=top_k)
    else:
        results = vector_store.search(q_embed, k=top_k)

    # 3. (Optional) rerank
    if rerank_fn:
        results = rerank_fn(question, results)[:top_k]

    # 4. Build context for prompt
    context = "\n\n".join([r["text"] for r in results])
    if prompt_template is None:
        prompt_template = DEFAULT_PROMPT_TEMPLATE
    prompt = prompt_template.format(context=context, question=question)

    # 5. Generate answer with local LLM (no API key required!)
    llm = get_llm(llm_name)
    answer = llm.generate(prompt)

    return {
        "answer": answer,
        "chunks": results,
        "question": question,
        "context": context,
        "prompt": prompt
    }
