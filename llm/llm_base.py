class LLMBase:
    def generate(self, prompt: str, max_new_tokens: int = 200, **kwargs) -> str:
        raise NotImplementedError("Must implement in subclass.")