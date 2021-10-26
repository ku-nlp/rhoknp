import re
import weakref
from functools import cached_property
from typing import TYPE_CHECKING, Optional

from .morpheme import Morpheme
from .unit import Unit
from .utils import DepType, Features, Rels

if TYPE_CHECKING:
    from .chunk import Chunk
    from .clause import Clause
    from .document import Document
    from .sentence import Sentence


class Phrase(Unit):
    """基本句クラス．

    Args:
        parent_index: 係り先の基本句の文内におけるインデックス．
        dep_type: 係り受けの種類．
        features: 素性．
        rels: 基本句間関係．
    """

    KNP_PATTERN = re.compile(
        fr"^\+ (?P<pid>-1|\d+)(?P<dtype>[{''.join(e.value for e in DepType)}])( (?P<tags>(<[^>]+>)*))?$"
    )
    count = 0

    def __init__(
        self, parent_index: int, dep_type: DepType, features: Features, rels: Rels
    ):
        super().__init__()

        # parent unit
        self._chunk: Optional["Chunk"] = None

        # child units
        self._morphemes: Optional[list[Morpheme]] = None

        self.parent_index: int = parent_index  #: 係り先の基本句の文内におけるインデックス．
        self.dep_type: DepType = dep_type  #: 係り受けの種類．
        self.features: Features = features  #: 素性．
        self.rels: Rels = rels  #: 基本句間関係．

        self.index = self.count
        Phrase.count += 1

    @property
    def parent_unit(self) -> Optional["Chunk"]:
        """上位の言語単位（文節）．未登録なら None．"""
        return self._chunk

    @property
    def child_units(self) -> Optional[list[Morpheme]]:
        """下位の言語単位（形態素）．解析結果にアクセスできないなら None．"""
        return self._morphemes

    @property
    def document(self) -> "Document":
        """文書．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return self.chunk.document

    @property
    def sentence(self) -> "Sentence":
        """文．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return self.chunk.sentence

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
        if self._chunk is None:
            raise AttributeError("chunk has not been set")
        return self._chunk

    @chunk.setter
    def chunk(self, chunk: "Chunk") -> None:
        """文節．

        Args:
            chunk: 文節．
        """
        self._chunk = chunk

    @property
    def morphemes(self) -> list[Morpheme]:
        """形態素．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._morphemes is None:
            raise AttributeError("morphemes have not been set")
        return self._morphemes

    @morphemes.setter
    def morphemes(self, morphemes: list[Morpheme]) -> None:
        """形態素．

        Args:
            morphemes: 形態素．
        """
        for morpheme in morphemes:
            morpheme.phrase = weakref.proxy(self)
        self._morphemes = morphemes

    @cached_property
    def head(self) -> Morpheme:
        """主辞の形態素．"""
        head = None
        for morpheme in self.morphemes:
            if morpheme.features is None:
                continue
            if "内容語" in morpheme.features and head is None:
                # Consider the first content word as the head
                head = morpheme
            if "準内容語" in morpheme.features:
                # Sub-content words overwrite the head
                head = morpheme
        if head:
            return head
        return self.morphemes[0]

    @property
    def parent(self) -> Optional["Phrase"]:
        """係り先の基本句．ないなら None．"""
        if self.parent_index == -1:
            return None
        return self.sentence.phrases[self.parent_index]

    @cached_property
    def children(self) -> list["Phrase"]:
        """この基本句に係っている基本句のリスト．"""
        return [phrase for phrase in self.sentence.phrases if phrase.parent == self]

    @classmethod
    def from_knp(cls, knp_text: str) -> "Phrase":
        """基本句クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．
        """
        first_line, *lines = knp_text.split("\n")
        match = cls.KNP_PATTERN.match(first_line)
        if match is None:
            raise ValueError(f"malformed line: {first_line}")
        parent_index = int(match.group("pid"))
        dep_type = DepType(match.group("dtype"))
        features = Features(match.group("tags") or "")
        rels = Rels.from_fstring(match.group("tags") or "")
        phrase = cls(parent_index, dep_type, features, rels)

        morphemes: list[Morpheme] = []
        for line in lines:
            if not line.strip():
                continue
            morpheme = Morpheme.from_jumanpp(line)
            morphemes.append(morpheme)
        phrase.morphemes = morphemes
        return phrase

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        ret = f"+ {self.parent_index}{self.dep_type.value}"
        if self.features:
            ret += f" {self.features}"
        ret += "\n"
        ret += "".join(morpheme.to_jumanpp() for morpheme in self.morphemes)
        return ret
