import re
import weakref
from functools import cached_property
from typing import TYPE_CHECKING, Optional

from .morpheme import Morpheme
from .phrase import Phrase
from .unit import Unit
from .utils import DepType, Features

if TYPE_CHECKING:
    from .clause import Clause
    from .document import Document
    from .sentence import Sentence


class Chunk(Unit):
    """文節クラス．

    Args:
        parent_index: 係り先の文節の文内におけるインデックス．
        dep_type: 係り受けの種類．
        features: 素性．

    Attributes:
        parent_index (int): 係り先の文節の文内におけるインデックス．
        dep_type (:class:`DepType`): 係り受けの種類．
        features (:class:`Features`): 素性．
    """

    KNP_PATTERN: re.Pattern = re.compile(
        fr"^\* (?P<pid>-1|\d+)(?P<dtype>[DPAI])( {Features.PATTERN.pattern})?$"
    )
    count = 0

    def __init__(self, parent_index: int, dep_type: DepType, features: Features):
        super().__init__()

        # parent unit
        self._clause: Optional["Clause"] = None

        # child units
        self._phrases: Optional[list[Phrase]] = None

        self.parent_index: int = parent_index
        self.dep_type: DepType = dep_type
        self.features: Features = features

        self.index = self.count
        Chunk.count += 1

    @property
    def parent_unit(self) -> Optional["Clause"]:
        """上位の言語単位（節）．未登録なら None．"""
        return self._clause

    @property
    def child_units(self) -> Optional[list[Phrase]]:
        """下位の言語単位（基本句）．解析結果にアクセスできないなら None．"""
        return self._phrases

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
        return self.clause.sentence

    @property
    def clause(self) -> "Clause":
        """節．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._clause is None:
            raise AttributeError("clause has not been set")
        return self._clause

    @clause.setter
    def clause(self, clause: "Clause") -> None:
        """節．

        Args:
            clause: 節．
        """
        self._clause = clause

    @property
    def phrases(self) -> list[Phrase]:
        """基本句のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._phrases is None:
            raise AttributeError("phrases have not been set")
        return self._phrases

    @phrases.setter
    def phrases(self, phrases: list[Phrase]) -> None:
        """基本句．

        Args:
            phrases: 基本句．
        """
        for phrase in phrases:
            phrase.chunk = weakref.proxy(self)
        self._phrases = phrases

    @property
    def morphemes(self) -> list[Morpheme]:
        """形態素のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]

    @property
    def parent(self) -> Optional["Chunk"]:
        """係り先の文節．ないなら None．"""
        if self.parent_index == -1:
            return None
        return self.sentence.chunks[self.parent_index]

    @cached_property
    def children(self) -> list["Chunk"]:
        """この文節に係っている文節のリスト．"""
        return [chunk for chunk in self.sentence.chunks if chunk.parent == self]

    @classmethod
    def from_knp(cls, knp_text: str) -> "Chunk":
        """文節クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．
        """
        first_line, *lines = knp_text.split("\n")
        match = cls.KNP_PATTERN.match(first_line)
        if match is None:
            raise ValueError(f"malformed line: {first_line}")
        parent_index = int(match.group("pid"))
        dep_type = DepType(match.group("dtype"))
        features = Features(match.group("feats") or "")
        chunk = cls(parent_index, dep_type, features)

        phrases: list[Phrase] = []
        phrase_lines: list[str] = []
        for line in lines:
            if not line.strip():
                continue
            if line.startswith("+") and phrase_lines:
                phrase = Phrase.from_knp("\n".join(phrase_lines))
                phrases.append(phrase)
                phrase_lines = []
            phrase_lines.append(line)
        else:
            phrase = Phrase.from_knp("\n".join(phrase_lines))
            phrases.append(phrase)
        chunk.phrases = phrases
        return chunk

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        ret = f"* {self.parent_index}{self.dep_type.value}"
        if self.features:
            ret += f" {self.features}"
        ret += "\n"
        ret += "".join(phrase.to_knp() for phrase in self.phrases)
        return ret
