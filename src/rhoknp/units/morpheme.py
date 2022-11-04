import re
from dataclasses import astuple, dataclass, fields
from functools import cached_property
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional, Tuple, Union

from rhoknp.props.feature import FeatureDict
from rhoknp.props.semantics import SemanticsDict
from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.base_phrase import BasePhrase
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document
    from rhoknp.units.phrase import Phrase
    from rhoknp.units.sentence import Sentence


@dataclass
class MorphemeAttributes:
    """形態素の属性クラス．"""

    PAT = re.compile(r"([^ ]+| [^ ]*) ([^ ]+| [^ ]*) ([^ ]+) (\d+) ([^ ]+) (\d+) ([^ ]+) (\d+) ([^ ]+) (\d+)")
    PAT_REPEATED = re.compile(r"(?P<pat>.+) ((?P=pat)) ([^ ]+) (\d+) ([^ ]+) (\d+) ([^ ]+) (\d+) ([^ ]+) (\d+)")

    reading: str  #: 読み．
    lemma: str  #: 原形．
    pos: str  #: 品詞．
    pos_id: int  #: 品詞ID．
    subpos: str  #: 品詞細分類．
    subpos_id: int  #: 品詞細分類ID．
    conjtype: str  #: 活用型．
    conjtype_id: int  #: 活用型ID．
    conjform: str  #: 活用形ID．
    conjform_id: int  #: 活用形ID．

    @classmethod
    def from_jumanpp(cls, jumanpp_line: str) -> "MorphemeAttributes":
        """形態素の属性クラスのインスタンスを Juman++ の解析結果から初期化．

        Args:
            jumanpp_line: Juman++ の解析結果．
        """
        kwargs = {}
        match = cls.PAT.match(jumanpp_line) or cls.PAT_REPEATED.match(jumanpp_line)
        assert match is not None
        for field, value in zip(fields(cls), match.groups()):
            kwargs[field.name] = field.type(value)
        assert len(kwargs) == len(fields(cls))
        return cls(**kwargs)

    def to_jumanpp(self) -> str:
        """Juman++ フォーマットに変換．"""
        return " ".join(str(item) for item in astuple(self))


class Morpheme(Unit):
    """形態素クラス．"""

    PAT: ClassVar[re.Pattern] = re.compile(
        r"(?P<surf>^([^ ]+| [^ ]*))"
        + rf"( (?P<attrs>{MorphemeAttributes.PAT.pattern}))"
        + rf"( {SemanticsDict.PAT.pattern})?"
        + rf"( {FeatureDict.PAT.pattern})?$"
    )

    PAT_REPEATED: ClassVar[re.Pattern] = re.compile(
        r"(?P<surf>.+) (?P<attrs>(?P=surf) (?P=surf) [^ ]+ \d+ [^ ]+ \d+ [^ ]+ \d+ [^ ]+ \d+)"
        + rf"( {SemanticsDict.PAT.pattern})?"
        + rf"( {FeatureDict.PAT.pattern})?$"
    )

    count = 0

    def __init__(
        self,
        text: str,
        attributes: Optional[MorphemeAttributes] = None,
        semantics: Optional[SemanticsDict] = None,
        features: Optional[FeatureDict] = None,
        homograph: bool = False,
    ) -> None:
        super().__init__()
        self.text = text

        # parent unit
        self._base_phrase: Optional["BasePhrase"] = None
        self._sentence: Optional["Sentence"] = None

        self.attributes: Optional[MorphemeAttributes] = attributes
        self.semantics: SemanticsDict = semantics if semantics is not None else SemanticsDict()  #: 辞書に記載の意味情報．
        self.features: FeatureDict = features if features is not None else FeatureDict()  #: 素性．
        self.homographs: List["Morpheme"] = []  #: 同形の形態素のリスト．

        self.index = self.count  #: 文内におけるインデックス．
        if homograph is False:
            Morpheme.count += 1

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
            return self.sentence.morphemes[self.index - 1].global_index + 1
        if self.sentence.index == 0:
            return self.index
        return self.document.sentences[self.sentence.index - 1].morphemes[-1].global_index + 1

    @property
    def parent_unit(self) -> Optional[Union["BasePhrase", "Sentence"]]:
        """上位の言語単位（基本句もしくは文）．未登録なら None．

        ..note::
            KNP によって解析済みなら基本句， Jumanpp によって解析済みなら文を返却．
        """
        if self._base_phrase is not None:
            return self._base_phrase
        if self._sentence is not None:
            return self._sentence
        return None

    @property
    def child_units(self) -> None:
        """下位の言語単位のリスト．形態素は最下位の言語単位なので常に None．"""
        return None

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
        return self._sentence or self.base_phrase.sentence

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
        return self.base_phrase.clause

    @property
    def phrase(self) -> "Phrase":
        """文節．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return self.base_phrase.phrase

    @property
    def base_phrase(self) -> "BasePhrase":
        """基本句．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._base_phrase is None:
            raise AttributeError("not available before applying KNP")
        return self._base_phrase

    @base_phrase.setter
    def base_phrase(self, base_phrase: "BasePhrase") -> None:
        """基本句．

        Args:
            base_phrase: 基本句．
        """
        self._base_phrase = base_phrase

    @property
    def surf(self) -> str:
        """表層表現．"""
        return self.text

    @property
    def reading(self) -> str:
        """読み．"""
        if self.attributes is None:
            raise AttributeError("attributes have not been set")
        return self.attributes.reading

    @property
    def lemma(self) -> str:
        """原形．"""
        if self.attributes is None:
            raise AttributeError("attributes have not been set")
        return self.attributes.lemma

    @property
    def canon(self) -> Optional[str]:
        """代表表記．"""
        canon = self.semantics.get("代表表記")
        assert canon is None or isinstance(canon, str)
        return canon

    @property
    def pos(self) -> str:
        """品詞．"""
        if self.attributes is None:
            raise AttributeError("attributes have not been set")
        return self.attributes.pos

    @property
    def subpos(self) -> str:
        """品詞細分類．"""
        if self.attributes is None:
            raise AttributeError("attributes have not been set")
        return self.attributes.subpos

    @property
    def conjtype(self) -> str:
        """活用型．"""
        if self.attributes is None:
            raise AttributeError("attributes have not been set")
        return self.attributes.conjtype

    @property
    def conjform(self) -> str:
        """活用形．"""
        if self.attributes is None:
            raise AttributeError("attributes have not been set")
        return self.attributes.conjform

    @property
    def sstring(self) -> str:
        """Juman++ フォーマットの意味情報．"""
        return self.semantics.to_sstring()

    @property
    def fstring(self) -> str:
        """Juman++ フォーマットの素性．"""
        return self.features.to_fstring()

    @cached_property
    def parent(self) -> Optional["Morpheme"]:
        """係り先の形態素．ないなら None．"""
        if self.base_phrase.head == self:
            if self.base_phrase.parent is not None:
                return self.base_phrase.parent.head
            return None
        return self.base_phrase.head

    @cached_property
    def span(self) -> Tuple[int, int]:
        """文における文字レベルのスパン．"""
        if self.index == 0:
            start = 0
        else:
            _, start = self.sentence.morphemes[self.index - 1].span
        end = start + len(self.text)  # TODO: correctly handle multibyte characters
        return start, end

    @cached_property
    def global_span(self) -> Tuple[int, int]:
        """文書全体における文字レベルのスパン．"""
        offset = 0
        for prev_sentence in self.document.sentences[: self.sentence.index]:
            offset += len(prev_sentence.text)
        start, end = self.span
        return start + offset, end + offset

    @cached_property
    def children(self) -> List["Morpheme"]:
        """この形態素に係っている形態素のリスト．"""
        return [morpheme for morpheme in self.sentence.morphemes if morpheme.parent == self]

    @classmethod
    def from_jumanpp(cls, jumanpp_text: str) -> "Morpheme":
        """形態素クラスのインスタンスを Juman++ の解析結果から初期化．

        Args:
            jumanpp_text: Juman++ の解析結果．
        """
        first_line, *lines = jumanpp_text.rstrip().split("\n")
        morpheme = cls._from_jumanpp_line(first_line)
        for line in lines:
            assert cls.is_homograph_line(line)
            homograph = cls._from_jumanpp_line(line[2:], homograph=True)
            morpheme.homographs.append(homograph)
        return morpheme

    @classmethod
    def _from_jumanpp_line(cls, jumanpp_line: str, homograph: bool = False) -> "Morpheme":
        """形態素クラスのインスタンスを Juman++ の解析結果から初期化．

        Args:
            jumanpp_line: Juman++ の解析結果．
            homograph: 同形かどうかを表すフラグ．
        """
        if (match := cls.PAT.match(jumanpp_line) or cls.PAT_REPEATED.match(jumanpp_line)) is None:
            raise ValueError(f"malformed morpheme line: {jumanpp_line}")
        surf = match["surf"]
        attributes = match["attrs"] and MorphemeAttributes.from_jumanpp(match["attrs"])
        semantics = SemanticsDict.from_sstring(match["sems"] or "")
        features = FeatureDict.from_fstring(match["feats"] or "")
        return cls(surf, attributes, semantics, features, homograph=homograph)

    def to_jumanpp(self) -> str:
        """Juman++ フォーマットに変換．"""
        ret = self.text
        if self.attributes is None:
            raise AttributeError("attributes have not been set")
        ret += f" {self.attributes.to_jumanpp()}"
        if self.semantics or self.semantics.is_nil is True:
            ret += f" {self.semantics.to_sstring()}"
        if self.features:
            ret += f" {self.features.to_fstring()}"
        ret += "\n"
        for homograph in self.homographs:
            ret += f"@ {homograph.to_jumanpp()}"
        return ret

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        ret = self.text
        if self.attributes is None:
            raise AttributeError("attributes have not been set")
        ret += f" {self.attributes.to_jumanpp()}"
        if self.semantics or self.semantics.is_nil is True:
            ret += f" {self.semantics.to_sstring()}"
        features = FeatureDict(self.features)
        for homograph in self.homographs:
            assert homograph.attributes is not None
            alt_feature_key = "ALT-{}-{}-{}-{}-{}-{}-{}-{}".format(
                homograph.surf,
                homograph.reading,
                homograph.lemma,
                homograph.attributes.pos_id,
                homograph.attributes.subpos_id,
                homograph.attributes.conjtype_id,
                homograph.attributes.conjform_id,
                homograph.semantics.to_sstring(),
            )
            features[alt_feature_key] = True
        if features:
            ret += f" {features.to_fstring()}"
        ret += "\n"
        return ret

    @staticmethod
    def is_morpheme_line(line: str) -> bool:
        """形態素行なら True を返す．"""
        return Morpheme.PAT.match(line) is not None or Morpheme.PAT_REPEATED.match(line) is not None

    @staticmethod
    def is_homograph_line(line: str) -> bool:
        """同形行なら True を返す．"""
        return line.startswith("@") and Morpheme.is_morpheme_line(line[2:])
