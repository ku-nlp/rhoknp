import re
import weakref
from functools import cached_property
from typing import TYPE_CHECKING, Optional, Union

from rhoknp.units.base_phrase import BasePhrase
from rhoknp.units.morpheme import Morpheme
from rhoknp.units.unit import Unit
from rhoknp.units.utils import DepType, Features

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document
    from rhoknp.units.sentence import Sentence


class Phrase(Unit):
    """文節クラス．"""

    KNP_PAT = re.compile(
        rf"^\* (?P<pid>-1|\d+)(?P<dtype>[DPAI])( {Features.PAT.pattern})?$"
    )
    count = 0

    def __init__(self, parent_index: int, dep_type: DepType, features: Features):
        super().__init__()

        # parent unit
        self._clause: Optional["Clause"] = None
        self._sentence: Optional["Sentence"] = None

        # child units
        self._base_phrases: Optional[list[BasePhrase]] = None

        self.parent_index: int = parent_index  #: 係り先の文節の文内におけるインデックス．
        self.dep_type: DepType = dep_type  #: 係り受けの種類．
        self.features: Features = features  #: 素性．

        self.index = self.count
        Phrase.count += 1

    @property
    def global_index(self) -> int:
        """文書全体におけるインデックス．"""
        offset = 0
        for prev_sentence in self.document.sentences[: self.sentence.index]:
            offset += len(prev_sentence.phrases)
        return self.index + offset

    @property
    def parent_unit(self) -> Optional[Union["Clause", "Sentence"]]:
        """上位の言語単位（節もしくは文）．未登録なら None．"""
        if self._clause is not None:
            return self._clause
        if self._sentence is not None:
            return self._sentence
        return None

    @property
    def child_units(self) -> Optional[list[BasePhrase]]:
        """下位の言語単位（基本句）．解析結果にアクセスできないなら None．"""
        return self._base_phrases

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
    def base_phrases(self) -> list[BasePhrase]:
        """基本句のリスト．"""
        if self._base_phrases is None:
            raise AssertionError
        return self._base_phrases

    @base_phrases.setter
    def base_phrases(self, base_phrases: list[BasePhrase]) -> None:
        """基本句．

        Args:
            base_phrases: 基本句．
        """
        for base_phrase in base_phrases:
            base_phrase.phrase = weakref.proxy(self)
        self._base_phrases = base_phrases

    @property
    def morphemes(self) -> list[Morpheme]:
        """形態素のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [
            morpheme
            for base_phrase in self.base_phrases
            for morpheme in base_phrase.morphemes
        ]

    @property
    def parent(self) -> Optional["Phrase"]:
        """係り先の文節．ないなら None．"""
        if self.parent_index == -1:
            return None
        return self.sentence.phrases[self.parent_index]

    @cached_property
    def children(self) -> list["Phrase"]:
        """この文節に係っている文節のリスト．"""
        return [phrase for phrase in self.sentence.phrases if phrase.parent == self]

    @classmethod
    def from_knp(cls, knp_text: str) -> "Phrase":
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
        phrase = cls(parent_index, dep_type, features)

        base_phrases: list[BasePhrase] = []
        base_phrase_lines: list[str] = []
        for line in lines:
            if not line.strip():
                continue
            if line.startswith("+") and base_phrase_lines:
                base_phrases.append(BasePhrase.from_knp("\n".join(base_phrase_lines)))
                base_phrase_lines = []
            base_phrase_lines.append(line)
        else:
            base_phrases.append(BasePhrase.from_knp("\n".join(base_phrase_lines)))
        phrase.base_phrases = base_phrases
        return phrase

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        ret = f"* {self.parent_index}{self.dep_type.value}"
        if self.features:
            ret += f" {self.features}"
        ret += "\n"
        ret += "".join(base_phrase.to_knp() for base_phrase in self.base_phrases)
        return ret
