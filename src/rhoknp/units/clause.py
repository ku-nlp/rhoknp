import weakref
from functools import cached_property
from typing import TYPE_CHECKING, Optional

from .chunk import Chunk
from .morpheme import Morpheme
from .phrase import Phrase
from .unit import Unit

if TYPE_CHECKING:
    from .document import Document
    from .sentence import Sentence


class Clause(Unit):
    """節クラス．"""

    count = 0

    def __init__(self):
        super().__init__()

        # parent unit
        self._sentence: Optional["Sentence"] = None

        # child units
        self._chunks: Optional[list[Chunk]] = None

        self.index = self.count
        Clause.count += 1

    @property
    def parent_unit(self) -> Optional["Sentence"]:
        """上位の言語単位（文）．未登録なら None．"""
        return self._sentence

    @property
    def child_units(self) -> Optional[list[Chunk]]:
        """下位の言語単位（文節）．解析結果にアクセスできないなら None．"""
        return self._chunks

    @property
    def document(self) -> "Document":
        """文書．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return self.sentence.document

    @property
    def sentence(self) -> "Sentence":
        """文．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self.parent_unit is None:
            raise AttributeError("sentence has not been set")
        return self.parent_unit

    @sentence.setter
    def sentence(self, sentence: "Sentence") -> None:
        """文．

        Args:
            sentence: 文．
        """
        self._sentence = sentence

    @property
    def chunks(self) -> list[Chunk]:
        """文節のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._chunks is None:
            raise AttributeError("chunks have not been set")
        return self._chunks

    @chunks.setter
    def chunks(self, chunks: list[Chunk]):
        """文節のリスト．

        Args:
            chunks: 文節のリスト．
        """
        for chunk in chunks:
            chunk.clause = weakref.proxy(self)
        self._chunks = chunks

    @property
    def phrases(self) -> list[Phrase]:
        """基本句のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self) -> list[Morpheme]:
        """形態素のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]

    @cached_property
    def head(self) -> Phrase:
        """節主辞の基本句．"""
        for phrase in self.phrases:
            if phrase.features and "節-主辞" in phrase.features:
                return phrase
        raise AssertionError

    @cached_property
    def parent(self) -> Optional["Clause"]:
        """係り先の節．ないなら None．"""
        head_parent = self.head.parent
        while head_parent in self.phrases:
            head_parent = head_parent.parent
        for clause in self.sentence.clauses:
            if head_parent in clause.phrases:
                return clause
        return None

    @cached_property
    def children(self) -> list["Clause"]:
        """この節に係っている節のリスト．"""
        return [clause for clause in self.sentence.clauses if clause.parent == self]

    @classmethod
    def from_knp(cls, knp_text: str) -> "Clause":
        """節クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．
        """
        clause = cls()
        chunks = []
        chunk_lines: list[str] = []
        for line in knp_text.split("\n"):
            if not line.strip():
                continue
            if line.startswith("*") and chunk_lines:
                chunk = Chunk.from_knp("\n".join(chunk_lines))
                chunks.append(chunk)
                chunk_lines = []
            chunk_lines.append(line)
        else:
            chunk = Chunk.from_knp("\n".join(chunk_lines))
            chunks.append(chunk)
        clause.chunks = chunks
        return clause

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        return "".join(chunk.to_knp() for chunk in self.chunks)
