from abc import ABC, abstractmethod
from typing import Union, overload

from rhoknp.units import Document, Sentence


class Processor(ABC):
    """解析器の基底クラス．"""

    @overload
    def __call__(self, text: str, timeout: int = 10) -> Document:
        ...

    @overload
    def __call__(self, text: Sentence, timeout: int = 10) -> Sentence:
        ...

    @overload
    def __call__(self, text: Document, timeout: int = 10) -> Document:
        ...

    def __call__(self, text: Union[str, Sentence, Document], timeout: int = 10) -> Union[Document, Sentence]:
        """テキストに解析器を適用する．

        Args:
            text: 解析するテキスト．
            timeout: 最大処理時間．

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
    def apply(self, text: str, timeout: int = 10) -> Document:
        ...

    @overload
    def apply(self, text: Sentence, timeout: int = 10) -> Sentence:
        ...

    @overload
    def apply(self, text: Document, timeout: int = 10) -> Document:
        ...

    def apply(self, text: Union[str, Sentence, Document], timeout: int = 10) -> Union[Document, Sentence]:
        """テキストに解析器を適用する．

        Args:
            text: 解析するテキスト．
            timeout: 最大処理時間．

        Raises:
            TypeError: textの型がstr, Sentence, Document以外の場合．

        .. note::
            このメソッドは引数の型に応じて ``apply_to_document`` または ``apply_to_sentence`` を呼び出す．
            引数の型が ``str`` の場合は ``apply_to_document`` を呼び出す．
            引数の型が ``Sentence`` の場合は ``apply_to_sentence`` を呼び出す．
            引数の型が ``Document`` の場合は ``apply_to_document`` を呼び出す．
        """
        if isinstance(text, str) or isinstance(text, Document):
            return self.apply_to_document(text, timeout=timeout)
        elif isinstance(text, Sentence):
            return self.apply_to_sentence(text, timeout=timeout)
        else:
            raise TypeError("Invalid type: text must be str, Sentence, or Document")

    @abstractmethod
    def apply_to_document(self, document: Union[Document, str], timeout: int = 10) -> Document:
        """文書に解析器を適用する．

        Args:
            document: 文書．
            timeout: 最大処理時間．
        """
        raise NotImplementedError

    @abstractmethod
    def apply_to_sentence(self, sentence: Union[Sentence, str], timeout: int = 10) -> Sentence:
        """文に解析器を適用する．

        Args:
            sentence: 文．
            timeout: 最大処理時間．
        """
        raise NotImplementedError
