from abc import ABC, abstractmethod
from multiprocessing import Pool
from typing import Union

from rhoknp.units.document import Document, Sentence


class Processor(ABC):
    @abstractmethod
    def apply_to_document(self, document: Union[Document, str]) -> Document:
        raise NotImplementedError

    @abstractmethod
    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        raise NotImplementedError

    def apply(self, document: Union[Document, str]) -> Document:
        return self.apply_to_document(document)

    def batch_apply(self, documents: list[Union[Document, str]], processes: int = 0) -> list[Document]:
        if processes < 1:
            return list(map(self.apply, documents))

        with Pool(processes=processes) as pool:
            return pool.map(self.apply, documents)
