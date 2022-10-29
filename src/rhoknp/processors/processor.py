from abc import ABC, abstractmethod
from typing import Union, overload

from rhoknp.units import Document, Sentence


class Processor(ABC):
    """解析器の基底クラス．"""

    @overload
    def __call__(self, text: str) -> Document:
        ...

    @overload
    def __call__(self, text: Sentence) -> Sentence:
        ...

    @overload
    def __call__(self, text: Document) -> Document:
        ...

    def __call__(self, text: Union[str, Sentence, Document]) -> Union[Document, Sentence]:
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
        return self.apply(text)

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

    @abstractmethod
    def apply_to_document(self, document: Union[Document, str]) -> Document:
        """文書に解析器を適用する．

        Args:
            document: 文書．
        """
        raise NotImplementedError

    @abstractmethod
    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に解析器を適用する．

        Args:
            sentence: 文．
        """
        raise NotImplementedError
