from llm import get_llm

def test_llm_generate_basic():
    llm = get_llm(model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0") 
    prompt = "Explain what a machine learning model is."
    result = llm.generate(prompt, max_new_tokens=50)
    print("LLM Output:", result)
    assert isinstance(result, str)
    assert len(result) > 10