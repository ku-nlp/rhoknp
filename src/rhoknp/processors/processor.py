from abc import ABC, abstractmethod
from multiprocessing import Pool
from typing import Union

from rhoknp.units.document import Document, Sentence


class Processor(ABC):
    @abstractmethod
    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        raise NotImplementedError

    def apply(self, document: Document) -> Document:
        raise NotImplementedError

    def batch_apply(self, documents: list[Document], processes: int = 0) -> list[Document]:
        if processes < 1:
            return list(map(self.apply, documents))

        with Pool(processes=processes) as pool:
            return pool.map(self.apply, documents)
