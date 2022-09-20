from abc import ABC, abstractmethod
from multiprocessing import Pool
from typing import List, Sequence, Union

from rhoknp.units import Document, Sentence


class Processor(ABC):
    """解析器の基底クラス．"""

    @abstractmethod
    def apply_to_document(self, document: Union[Document, str]) -> Document:
        """文書に解析器を適用する．"""
        raise NotImplementedError

    def batch_apply_to_documents(self, documents: Sequence[Union[Document, str]], processes: int = 0) -> List[Document]:
        """複数文書に解析器を適用する．"""
        if processes < 1:
            return list(map(self.apply_to_document, documents))
        with Pool(processes=processes) as pool:
            return pool.map(self.apply_to_document, documents)

    @abstractmethod
    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に解析器を適用する．"""
        raise NotImplementedError

    def batch_apply_to_sentences(self, sentences: Sequence[Union[Sentence, str]], processes: int = 0) -> List[Sentence]:
        """複数文に解析器を適用する．"""
        if processes < 1:
            return list(map(self.apply, sentences))
        with Pool(processes=processes) as pool:
            return pool.map(self.apply, sentences)

    def apply(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に解析器を適用する．"""
        return self.apply_to_sentence(sentence)

    def batch_apply(self, sentences: Sequence[Union[Sentence, str]], processes: int = 0) -> List[Sentence]:
        """複数文に解析器を適用する．"""
        return self.batch_apply_to_sentences(sentences, processes)
