from abc import ABC, abstractmethod
from typing import List, Dict

class SplitterBase(ABC):
    @abstractmethod
    def chunk(self, text: str, chunk_size: int, overlap: int) -> List[Dict]:
        pass
