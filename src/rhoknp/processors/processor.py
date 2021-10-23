from abc import ABC, abstractmethod
from multiprocessing import Pool
from typing import Sequence, Union

from rhoknp.units import Document, Sentence


class Processor(ABC):
    @abstractmethod
    def apply_to_document(self, document: Union[Document, str]) -> Document:
        raise NotImplementedError

    def batch_apply_to_documents(
        self, documents: Sequence[Union[Document, str]], processes: int = 0
    ) -> list[Document]:
        if processes < 1:
            return list(map(self.apply_to_document, documents))
        with Pool(processes=processes) as pool:
            return pool.map(self.apply_to_document, documents)

    @abstractmethod
    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        raise NotImplementedError

    def batch_apply_to_sentences(
        self, sentences: Sequence[Union[Sentence, str]], processes: int = 0
    ) -> list[Sentence]:
        if processes < 1:
            return list(map(self.apply, sentences))
        with Pool(processes=processes) as pool:
            return pool.map(self.apply, sentences)

    def apply(self, sentence: Union[Sentence, str]) -> Sentence:
        return self.apply_to_sentence(sentence)

    def batch_apply(
        self, sentences: Sequence[Union[Sentence, str]], processes: int = 0
    ) -> list[Sentence]:
        return self.batch_apply_to_sentences(sentences)
