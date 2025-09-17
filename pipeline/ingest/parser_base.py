from abc import ABC, abstractmethod

class ParserBase(ABC):
    @abstractmethod
    def extract_text_and_metadata(self, filepath: str) -> (str, dict):
        pass