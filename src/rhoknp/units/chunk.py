import re
import weakref
from functools import cached_property
from typing import TYPE_CHECKING, Optional, Union

from rhoknp.units.morpheme import Morpheme
from rhoknp.units.phrase import Phrase
from rhoknp.units.unit import Unit
from rhoknp.units.utils import DepType, Features

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document
    from rhoknp.units.sentence import Sentence


class Chunk(Unit):
    """文節クラス．"""

    KNP_PAT = re.compile(
        fr"^\* (?P<pid>-1|\d+)(?P<dtype>[DPAI])( {Features.PAT.pattern})?$"
    )
    count = 0

    def __init__(self, parent_index: int, dep_type: DepType, features: Features):
        super().__init__()

        # parent unit
        self._clause: Optional["Clause"] = None
        self._sentence: Optional["Sentence"] = None

        # child units
        self._phrases: Optional[list[Phrase]] = None

        self.parent_index: int = parent_index  #: 係り先の文節の文内におけるインデックス．
        self.dep_type: DepType = dep_type  #: 係り受けの種類．
        self.features: Features = features  #: 素性．

        self.index = self.count
        Chunk.count += 1

    @property
    def parent_unit(self) -> Optional[Union["Clause", "Sentence"]]:
        """上位の言語単位（節もしくは文）．未登録なら None．"""
        if self._clause is not None:
            return self._clause
        if self._sentence is not None:
            return self._sentence
        return None

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
        return self._sentence or self.clause.sentence

    @sentence.setter
    def sentence(self, sentence: "Sentence") -> None:
        """文．

        Args:
            sentence: 文．
        """
        self._sentence = sentence

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
        match = cls.KNP_PAT.match(first_line)
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
                phrases.append(Phrase.from_knp("\n".join(phrase_lines)))
                phrase_lines = []
            phrase_lines.append(line)
        else:
            phrases.append(Phrase.from_knp("\n".join(phrase_lines)))
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
