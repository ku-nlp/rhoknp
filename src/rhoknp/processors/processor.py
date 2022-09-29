from abc import ABC, abstractmethod
from multiprocessing import Pool
from typing import List, Sequence, Union, overload

from typing_extensions import TypeGuard

from rhoknp.units import Document, Sentence


def _is_sequence_of_str(seq: Sequence) -> TypeGuard[Sequence[str]]:
    return all(isinstance(x, str) for x in seq)


def _is_sequence_of_sentence(seq: Sequence) -> TypeGuard[Sequence[Sentence]]:
    return all(isinstance(x, Sentence) for x in seq)


def _is_sequence_of_document(seq: Sequence) -> TypeGuard[Sequence[Document]]:
    return all(isinstance(x, Document) for x in seq)


class Processor(ABC):
    """解析器の基底クラス．"""

    @overload
    def apply(self, text: str) -> Document:
        ...

    @overload
    def apply(self, text: Sentence) -> Sentence:
        ...

    @overload
    def apply(self, text: Document) -> Document:
        ...

    def apply(self, text: Union[str, Sentence, Document]) -> Union[Document, Sentence]:
        """テキストに解析器を適用する．

        Args:
            text: 解析するテキスト．

        Raises:
            TypeError: textの型がstr, Sentence, Document以外の場合．

        .. note::
            このメソッドは引数の型に応じて ``apply_to_document`` または ``apply_to_sentence`` を呼び出す．
            引数の型が ``str`` の場合は ``apply_to_document`` を呼び出す．
            引数の型が ``Sentence`` の場合は ``apply_to_sentence`` を呼び出す．
            引数の型が ``Document`` の場合は ``apply_to_document`` を呼び出す．
        """
        if isinstance(text, str):
            return self.apply_to_document(text)
        elif isinstance(text, Sentence):
            return self.apply_to_sentence(text)
        elif isinstance(text, Document):
            return self.apply_to_document(text)
        else:
            raise TypeError("Invalid type: text must be str, Sentence, or Document")

    @overload
    def batch_apply(self, texts: Sequence[str], processes: int = 0) -> List[Document]:
        ...

    @overload
    def batch_apply(self, texts: Sequence[Sentence], processes: int = 0) -> List[Sentence]:
        ...

    @overload
    def batch_apply(self, texts: Sequence[Document], processes: int = 0) -> List[Document]:
        ...

    def batch_apply(
        self,
        texts: Union[Sequence[str], Sequence[Sentence], Sequence[Document]],
        processes: int = 0,
    ) -> Union[List[Sentence], List[Document]]:
        """複数テキストに解析器を適用する．

        Args:
            texts: テキストのリスト．
            processes: 並列処理数．0以下の場合はシングルプロセスで処理する．

        Raises:
            TypeError: textsの型がstr, Sentence, Documentのリスト以外の場合．

        .. note::
            このメソッドは引数の型に応じて ``batch_apply_to_documents`` または ``batch_apply_to_sentences`` を呼び出す．
            引数の型が ``str`` のリストの場合は ``batch_apply_to_documents`` を呼び出す．
            引数の型が ``Sentence`` のリストの場合は ``batch_apply_to_sentences`` を呼び出す．
            引数の型が ``Document`` のリストの場合は ``batch_apply_to_documents`` を呼び出す．
        """
        if _is_sequence_of_str(texts):
            return self.batch_apply_to_documents(texts, processes)
        elif _is_sequence_of_sentence(texts):
            return self.batch_apply_to_sentences(texts, processes)
        elif _is_sequence_of_document(texts):
            return self.batch_apply_to_documents(texts, processes)
        else:
            raise TypeError("Invalid type: texts must be a sequence of str, Sentence, or Document")

    @abstractmethod
    def apply_to_document(self, document: Union[Document, str]) -> Document:
        """文書に解析器を適用する．

        Args:
            document: 文書．
        """
        raise NotImplementedError

    def batch_apply_to_documents(
        self,
        documents: Union[Sequence[Document], Sequence[str]],
        processes: int = 0,
    ) -> List[Document]:
        """複数文書に解析器を適用する．

        Args:
            documents: 文書のリスト．
            processes: 並列処理数．0以下の場合はシングルプロセスで処理する．

        Raises:
            TypeError: documentsの型がstr, Documentのリスト以外の場合．
        """
        if _is_sequence_of_str(documents) or _is_sequence_of_document(documents):
            if processes < 1:
                return list(map(self.apply_to_document, documents))
            with Pool(processes) as pool:
                return pool.map(self.apply_to_document, documents)
        raise TypeError("Invalid type: documents must be a sequence of str or Document")

    @abstractmethod
    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に解析器を適用する．

        Args:
            sentence: 文．
        """
        raise NotImplementedError

    def batch_apply_to_sentences(
        self,
        sentences: Union[Sequence[str], Sequence[Sentence]],
        processes: int = 0,
    ) -> List[Sentence]:
        """複数文に解析器を適用する．

        Args:
            sentences: 文のリスト．
            processes: 並列処理数．0以下の場合はシングルプロセスで処理する．

        Raises:
            TypeError: sentencesの型がstr, Sentenceのリスト以外の場合．
        """
        if _is_sequence_of_str(sentences) or _is_sequence_of_sentence(sentences):
            if processes < 1:
                return list(map(self.apply_to_sentence, sentences))
            with Pool(processes) as pool:
                return pool.map(self.apply_to_sentence, sentences)
        raise TypeError("Invalid type: sentences must be a sequence of str or Sentence")
