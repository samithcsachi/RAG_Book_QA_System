from llm.llm_base import LLMBase
from transformers import pipeline

class LocalLLM(LLMBase):
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0", device="cpu", **kwargs):
        self.pipe = pipeline("text-generation", model=model_name, device=device, **kwargs)
    def generate(self, prompt: str, max_new_tokens: int = 200, **kwargs) -> str:
        result = self.pipe(prompt, max_new_tokens=max_new_tokens)
        return result[0]["generated_text"]

def get_llm(model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0", **kwargs):
    
    return LocalLLM(model_name=model_name, **kwargs)
