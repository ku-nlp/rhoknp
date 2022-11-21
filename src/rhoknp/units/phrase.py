import re
from functools import cached_property
from typing import TYPE_CHECKING, Any, List, Optional, Union

from rhoknp.props.dependency import DepType
from rhoknp.props.feature import FeatureDict
from rhoknp.units.base_phrase import BasePhrase
from rhoknp.units.morpheme import Morpheme
from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document
    from rhoknp.units.sentence import Sentence


class Phrase(Unit):
    """文節クラス．"""

    PAT = re.compile(rf"^\*( (?P<pid>-1|\d+)(?P<dtype>[DPAI]))?( {FeatureDict.PAT.pattern})?$")
    count = 0

    def __init__(
        self,
        parent_index: Optional[int],
        dep_type: Optional[DepType],
        features: Optional[FeatureDict] = None,
    ):
        super().__init__()

        # parent unit
        self._clause: Optional["Clause"] = None
        self._sentence: Optional["Sentence"] = None

        # child units
        self._base_phrases: Optional[List[BasePhrase]] = None

        self.parent_index: Optional[int] = parent_index  #: 係り先の文節の文内におけるインデックス．
        self.dep_type: Optional[DepType] = dep_type  #: 係り受けの種類．
        self.features: FeatureDict = features or FeatureDict()  #: 素性．

        self.index = self.count  #: 文内におけるインデックス．
        Phrase.count += 1

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)) is False:
            return False
        if self.parent_unit != other.parent_unit:
            return False
        return self.index == other.index

    @cached_property
    def global_index(self) -> int:
        """文書全体におけるインデックス．"""
        if self.index > 0:
            return self.sentence.phrases[self.index - 1].global_index + 1
        if self.sentence.index == 0:
            return self.index
        return self.document.sentences[self.sentence.index - 1].phrases[-1].global_index + 1

    @property
    def parent_unit(self) -> Optional[Union["Clause", "Sentence"]]:
        """上位の言語単位（節もしくは文）．未登録なら None．"""
        if self._clause is not None:
            return self._clause
        if self._sentence is not None:
            return self._sentence
        return None

    @property
    def child_units(self) -> Optional[List[BasePhrase]]:
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
        """文．"""
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
    def base_phrases(self) -> List[BasePhrase]:
        """基本句のリスト．"""
        assert self._base_phrases is not None
        return self._base_phrases

    @base_phrases.setter
    def base_phrases(self, base_phrases: List[BasePhrase]) -> None:
        """基本句のリスト．

        Args:
            base_phrases: 基本句のリスト．
        """
        for base_phrase in base_phrases:
            base_phrase.phrase = self
        self._base_phrases = base_phrases

    @property
    def morphemes(self) -> List[Morpheme]:
        """形態素のリスト．"""
        return [morpheme for base_phrase in self.base_phrases for morpheme in base_phrase.morphemes]

    @property
    def parent(self) -> Optional["Phrase"]:
        """係り先の文節．ないなら None．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self.parent_index is None:
            raise AttributeError("parent_index has not been set")
        if self.parent_index == -1:
            return None
        return self.sentence.phrases[self.parent_index]

    @cached_property
    def children(self) -> List["Phrase"]:
        """この文節に係っている文節のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [phrase for phrase in self.sentence.phrases if phrase.parent == self]

    @classmethod
    def from_knp(cls, knp_text: str) -> "Phrase":
        """文節クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．

        Raises:
            ValueError: 解析結果読み込み中にエラーが発生した場合．
        """
        first_line, *lines = knp_text.split("\n")
        match = cls.PAT.match(first_line)
        if match is None:
            raise ValueError(f"malformed phrase line: {first_line}")
        parent_index = int(match["pid"]) if match["pid"] is not None else None
        dep_type = DepType(match["dtype"]) if match["dtype"] is not None else None
        features = FeatureDict.from_fstring(match["feats"] or "")
        phrase = cls(parent_index, dep_type, features)

        base_phrases: List[BasePhrase] = []
        base_phrase_lines: List[str] = []
        for line in lines:
            if line.strip() == "":
                continue
            if BasePhrase.is_base_phrase_line(line) and base_phrase_lines:
                base_phrases.append(BasePhrase.from_knp("\n".join(base_phrase_lines)))
                base_phrase_lines = []
            base_phrase_lines.append(line)
        else:
            base_phrases.append(BasePhrase.from_knp("\n".join(base_phrase_lines)))
        phrase.base_phrases = base_phrases
        return phrase

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        ret = "*"
        if self.parent_index is not None:
            assert self.dep_type is not None
            ret += f" {self.parent_index}{self.dep_type.value}"
        if self.features:
            ret += f" {self.features.to_fstring()}"
        ret += "\n"
        ret += "".join(base_phrase.to_knp() for base_phrase in self.base_phrases)
        return ret

    @staticmethod
    def is_phrase_line(line: str) -> bool:
        """文節行なら True を返す．"""
        return Phrase.PAT.match(line) is not None
