import re
from dataclasses import astuple, dataclass, fields
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, Optional, Union

from rhoknp.units.unit import Unit
from rhoknp.units.utils import Features, Semantics

if TYPE_CHECKING:
    from rhoknp.units.chunk import Chunk
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document
    from rhoknp.units.phrase import Phrase
    from rhoknp.units.sentence import Sentence


@dataclass(frozen=True)
class MorphemeAttributes:
    """形態素の属性クラス．

    Args:
        surf: 表層表現．
        reading: 読み．
        lemma: 原形．
        pos: 品詞．
        pos_id: 品詞ID．
        subpos: 品詞細分類．
        subpos_id: 品詞細分類ID．
        conjtype: 活用型．
        conjtype_id: 用型ID．
        conjform: 活用形ID．
        conjform_id: 活用形ID．
    """

    JUMANPP_PATTERN = re.compile(
        r"(?P<attrs>([^ ]+ [^ ]+ [^ ]+ \w+ \d+ \D+ \d+ \D+ \d+ \D+ \d+))"
    )

    surf: str  #: 表層表現．
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
        for field, value in zip(fields(cls), jumanpp_line.split(" ")):
            kwargs[field.name] = field.type(value)
        assert len(kwargs) == len(fields(cls)), f"malformed line: {jumanpp_line}"
        return cls(**kwargs)

    def to_jumanpp(self) -> str:
        """Juman++ フォーマットに変換．"""
        return " ".join(str(item) for item in astuple(self))


class Morpheme(Unit):
    """形態素クラス．

    Args:
        attributes: 属性．
        semantics: 辞書 (JumanDic) に記載の意味情報．
        features: 素性．
        homograph: 同形かどうかを表すフラグ．
    """

    JUMANPP_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        (
            rf"^({MorphemeAttributes.JUMANPP_PATTERN.pattern})"
            + rf"(\s{Semantics.PATTERN.pattern})?"
            + rf"(\s{Features.PATTERN.pattern})?$"
        )
    )

    count = 0

    def __init__(
        self,
        attributes: MorphemeAttributes,
        semantics: Semantics,
        features: Features,
        homograph: bool = False,
    ):
        super().__init__()

        # parent unit
        self._phrase: Optional["Phrase"] = None
        self._sentence: Optional["Sentence"] = None

        self._attributes = attributes
        self.semantics = semantics  #: 辞書 (JumanDic) に記載の意味情報．
        self.features = features  #: 素性．
        self.homographs: list["Morpheme"] = []  #: 同形の形態素のリスト．

        self.text = attributes.surf

        self.index = self.count
        if homograph is False:
            Morpheme.count += 1

    @property
    def parent_unit(self) -> Optional[Union["Phrase", "Sentence"]]:
        """上位の言語単位（基本句もしくは文）．未登録なら None．

        ..note::
            KNP によって解析済みなら基本句， Jumanpp によって解析済みなら文を返却．
        """
        if self._phrase is not None:
            return self._phrase
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
        if self._sentence is not None:
            return self._sentence
        if self._phrase is not None:
            return self.clause.sentence
        raise AttributeError("sentence has not been set")

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
        return self.chunk.clause

    @property
    def chunk(self) -> "Chunk":
        """文節．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return self.phrase.chunk

    @property
    def phrase(self) -> "Phrase":
        """基本句．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._phrase is None:
            raise AttributeError("not available before applying KNP")
        return self._phrase

    @phrase.setter
    def phrase(self, phrase: "Phrase") -> None:
        """基本句．

        Args:
            phrase: 基本句．
        """
        self._phrase = phrase

    @property
    def surf(self) -> str:
        """表層表現．"""
        return self._attributes.surf

    @property
    def reading(self) -> str:
        """読み．"""
        return self._attributes.reading

    @property
    def lemma(self) -> str:
        """原形．"""
        return self._attributes.lemma

    @property
    def canon(self) -> Optional[str]:
        """代表表記．"""
        canon = self.semantics.get("代表表記", None)
        assert canon is None or isinstance(canon, str)
        return canon

    @property
    def pos(self) -> str:
        """品詞．"""
        return self._attributes.pos

    @property
    def subpos(self) -> str:
        """品詞細分類．"""
        return self._attributes.subpos

    @property
    def conjtype(self) -> str:
        """活用型．"""
        return self._attributes.conjtype

    @property
    def conjform(self) -> str:
        """活用形．"""
        return self._attributes.conjform

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
        if self.phrase.head == self:
            if self.phrase.parent is not None:
                return self.phrase.parent.head
            return None
        return self.phrase.head

    @cached_property
    def span(self) -> tuple[int, int]:
        """文中での文字レベルのスパン．"""
        if self._sentence is None or self.index == 0:
            start = 0
        else:
            _, prev_end = self.sentence.morphemes[self.index - 1].span
            start = prev_end + 1
        end = start + len(self.text) - 1  # TODO: correctly handle multibyte characters
        return start, end

    @cached_property
    def children(self) -> list["Morpheme"]:
        """この形態素に係っている形態素のリスト．"""
        return [
            morpheme for morpheme in self.sentence.morphemes if morpheme.parent == self
        ]

    @classmethod
    def from_jumanpp(cls, jumanpp_text: str) -> "Morpheme":
        """形態素クラスのインスタンスを Juman++ の解析結果から初期化．

        Args:
            jumanpp_text: Juman++ の解析結果．
        """
        first_line, *lines = jumanpp_text.rstrip().split("\n")
        morpheme = cls._from_jumanpp_line(first_line)
        for line in lines:
            assert line.startswith("@ ")
            homograph = cls._from_jumanpp_line(line[2:], homograph=True)
            morpheme.homographs.append(homograph)
        return morpheme

    @classmethod
    def _from_jumanpp_line(
        cls, jumanpp_line: str, homograph: bool = False
    ) -> "Morpheme":
        """形態素クラスのインスタンスを Juman++ の解析結果から初期化．

        Args:
            jumanpp_line: Juman++ の解析結果．
            homograph: 同形かどうかを表すフラグ．
        """
        assert "\n" not in jumanpp_line.strip()
        match = cls.JUMANPP_PATTERN.match(jumanpp_line)
        if match is None:
            raise ValueError(f"malformed line: {jumanpp_line}")
        attributes = MorphemeAttributes.from_jumanpp(match.group("attrs"))
        semantics = Semantics.from_sstring(match.group("sems") or "")
        features = Features.from_fstring(match.group("feats") or "")
        return cls(attributes, semantics, features, homograph=homograph)

    def to_jumanpp(self) -> str:
        """Juman++ フォーマットに変換．"""
        ret = self._attributes.to_jumanpp()
        if self.semantics:
            ret += f" {self.semantics}"
        if self.features:
            ret += f" {self.features}"
        ret += "\n"
        for homograph in self.homographs:
            ret += f"@ {homograph.to_jumanpp()}"
        return ret
